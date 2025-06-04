from langgraph.graph import StateGraph, END
from llm.ollama_client import OllamaClient
from core.registry import AGENT_REGISTRY
from typing import TypedDict, Optional
from pydantic import BaseModel, Field
from langchain_core.outputs import LLMResult


class AgentResponseFormatter(BaseModel):
    """Always use this tool to structure your response to the user."""

    id: str = Field(description="agent id to route the request to")


class ChatStateDict(TypedDict):
    input_text: str
    agent_id: Optional[str]
    response: str


class ChatState:
    def __init__(self, input_text, agent_id=None):
        self.input_text = input_text
        self.agent_id = agent_id
        self.response = ""


async def entry_node(state: ChatStateDict):
    ollama = OllamaClient()

    # Build agent descriptions string
    agent_descriptions = "\n".join(
        [
            f"id: {agent_id}\ndescription: {data['description']}"
            for agent_id, data in AGENT_REGISTRY.items()
            if agent_id != "default"
        ]
    )

    prompt = f"""Route this request to the right agent.
Available agents:
{agent_descriptions}

Input: {state['input_text']}"""

    response = await ollama.generate(prompt=prompt, format=AgentResponseFormatter)

    try:
        import json

        if not isinstance(response, LLMResult):
            print("Response is not LLMResult, sending to default agent")
            return {"agent_id": "default"}
        # Loop through generations to handle GenerationChunk responses
        for generation in response.generations[0]:
            if hasattr(generation, "text"):
                parsed_response = json.loads(generation.text)
                agent_id = parsed_response["id"]
                break

        if agent_id not in AGENT_REGISTRY:
            print("Unknown agent: ", agent_id)
            print("Sending to default agent")
            return {"agent_id": "default"}

        print("Sending to agent: ", agent_id)
        return {"agent_id": agent_id}

    except Exception as e:
        print("Exception: ", e)
        print("Sending to default agent")
        return {"agent_id": "default"}


async def agent_node(state: ChatStateDict):
    agent_data = AGENT_REGISTRY[state["agent_id"]]
    agent = agent_data["instance"]
    response = await agent.run(state["input_text"], {})
    return {"response": response}


def create_graph():
    graph = StateGraph(ChatStateDict)
    graph.add_node("entry", entry_node)
    for agent_id in AGENT_REGISTRY.keys():
        graph.add_node(agent_id, agent_node)

    # Add conditional routing from entry to agent nodes
    graph.add_conditional_edges(
        "entry",
        lambda x: x["agent_id"],
        {agent_id: agent_id for agent_id in AGENT_REGISTRY.keys()},
    )

    # Add edges from all agent nodes to END
    for agent_id in AGENT_REGISTRY.keys():
        graph.add_edge(agent_id, END)

    graph.set_entry_point("entry")

    return graph.compile()
