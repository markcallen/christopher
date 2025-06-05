"""CLI for Christopher."""

import asyncio
import json
import logging
import uuid
from typing import TypedDict

import inquirer
import redis
from dotenv import load_dotenv
from langchain.schema.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph

from core.christopher import load_agents, run_with_langgraph

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Redis setup
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# checkpointer = InMemorySaver()


class GraphState(TypedDict):
    conversation_id: str
    messages: list[BaseMessage]
    user_input: str | None
    bot_output: str | None


# Node: get user input
def get_user_input(state):
    print(
        "Type /exit to quit, /archive to archive, /list to list, /switch <id> to switch"
    )
    user_input = input("You: ")
    return {"user_input": user_input}


# Node: save user input to redis and return message
def store_input(state):
    conv_id = state["conversation_id"]
    user_input = state["user_input"]
    redis_client.rpush(
        f"chat:{conv_id}", json.dumps({"role": "user", "content": user_input})
    )
    return {"messages": [HumanMessage(content=user_input)]}


# Node: store model output to redis
def store_response(state):
    conv_id = state["conversation_id"]
    redis_client.rpush(
        f"chat:{conv_id}",
        json.dumps({"role": "assistant", "content": state["bot_output"]}),
    )
    print(f"Bot: {state['bot_output']}")
    return {}


# Build LangGraph
builder = StateGraph(state_schema=GraphState)
builder.add_node("get_input", get_user_input)
builder.add_node("store_input", store_input)
builder.add_node("call_model", run_with_langgraph)
builder.add_node("store_response", store_response)

builder.set_entry_point("get_input")
builder.add_edge("get_input", "store_input")
builder.add_edge("store_input", "call_model")
builder.add_edge("call_model", "store_response")
builder.add_edge("store_response", "get_input")
builder.set_finish_point("store_response")

graph = builder.compile()


# CLI interface
async def chat(conv_id=None):
    if not conv_id:
        conv_id = str(uuid.uuid4())[:8]
        print(f"Started new conversation: {conv_id}")
    else:
        print(f"Resuming conversation: {conv_id}")

    state = {"conversation_id": conv_id, "messages": []}

    try:
        for output in graph.stream(state):
            updates = list(output.values())[-1]
            if "user_input" in updates:
                cmd = updates["user_input"].strip()
                if cmd == "/exit":
                    break
                elif cmd == "/archive":
                    msgs = redis_client.lrange(f"chat:{conv_id}", 0, -1)
                    for msg in msgs:
                        redis_client.rpush(f"chat:{conv_id}:archived", msg)
                    redis_client.delete(f"chat:{conv_id}")
                    print("Conversation archived.")
                    break
                elif cmd == "/list":
                    keys = redis_client.keys("chat:*")
                    convos = [
                        k.split(":")[1] for k in keys if not k.endswith(":archived")
                    ]
                    print("Conversations:", convos)
                elif cmd.startswith("/switch"):
                    _, new_id = cmd.split()
                    return chat(new_id)
    except KeyboardInterrupt:
        print("\nExiting.")


async def main():
    """Run the main CLI loop."""
    logger.info("Starting Christopher CLI")
    load_agents()
    logger.info("Agents loaded successfully")
    # thread_id = await inquirer.text("Thread ID (new or existing)")

    while True:
        user_input = inquirer.text(
            "You:"
        )  # Remove await since inquirer.text is not async
        logger.info(f"User input: {user_input}")

        if user_input.lower() in ["exit", "quit"]:
            logger.info("User requested exit")
            break

        try:
            logger.info("Processing user input with langgraph")
            response = await run_with_langgraph(user_input)
            logger.info(f"Generated response: {response}")
            print(f"Christopher: {response}")  # noqa: T201
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}", exc_info=True)
            logger.error(f"Error: {e}")

    logger.info("Christopher CLI session ended")


if __name__ == "__main__":
    asyncio.run(main())
