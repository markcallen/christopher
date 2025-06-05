"""LangGraph runner module for managing agent routing and execution."""

import json
import logging
from typing import Any, TypedDict

from langchain_core.outputs import LLMResult
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field

from core.registry import AGENT_REGISTRY
from llm.ollama_client import OllamaClient

# Configure logging
logger = logging.getLogger(__name__)


class AgentResponseFormatter(BaseModel):
    """Formatter for agent routing responses.

    This model ensures consistent response structure when routing requests to agents.
    """

    id: str = Field(description="agent id to route the request to")


class ChatStateDict(TypedDict):
    """Type definition for the chat state dictionary.

    Attributes
    ----------
        input_text: The user's input text
        agent_id: Optional ID of the agent to handle the request
        response: The agent's response text

    """

    input_text: str
    agent_id: str | None
    response: str


class ChatState:
    """Represents the state of a chat conversation.

    Attributes
    ----------
        input_text: The user's input text
        agent_id: Optional ID of the agent to handle the request
        response: The agent's response text

    """

    def __init__(self, input_text: str, agent_id: str | None = None) -> None:
        """Initialize a new chat state.

        Args:
        ----
            input_text: The user's input text
            agent_id: Optional ID of the agent to handle the request

        """
        self.input_text = input_text
        self.agent_id = agent_id
        self.response = ""


async def entry_node(state: ChatStateDict) -> dict[str, str]:
    """Route the input to the appropriate agent.

    Args:
    ----
        state: The current chat state containing the input text

    Returns:
    -------
        Dictionary containing the selected agent_id

    """
    ollama = OllamaClient()

    # Build agent descriptions string
    agent_descriptions = "\n".join(
        [
            f"{agent_id}: {data['description']}"
            for agent_id, data in AGENT_REGISTRY.items()
            if agent_id != "default"
        ]
    )

    prompt = f"""Route this request to the right agent.
Available agents:
{agent_descriptions}

Only return the id value of the agent that best matches the request.
Do not include any other text in your response.

Input: {state['input_text']}"""
    logger.debug(f"Agent routing prompt:\n{prompt}")

    response = await ollama.generate(prompt=prompt, format=AgentResponseFormatter)
    logger.debug(f"Agent routing response:\n{response}")

    try:
        if not isinstance(response, LLMResult):
            logger.warning("Response is not LLMResult, sending to default agent")
            return {"agent_id": "default"}

        # Loop through generations to handle GenerationChunk responses
        for generation in response.generations[0]:
            if hasattr(generation, "text"):
                parsed_response = json.loads(generation.text)
                agent_id = parsed_response["id"]
                break

        if agent_id not in AGENT_REGISTRY:
            logger.warning(f"Unknown agent: {agent_id}, sending to default agent")
            return {"agent_id": "default"}

        logger.info(f"Sending to agent: {agent_id}")
        return {"agent_id": agent_id}

    except Exception as e:
        logger.error(f"Exception during agent routing: {e}")
        return {"agent_id": "default"}


async def agent_node(state: ChatStateDict) -> dict[str, str]:
    """Process the input using the selected agent.

    Args:
    ----
        state: The current chat state containing the input text and agent_id

    Returns:
    -------
        Dictionary containing the agent's response

    """
    agent_id = state["agent_id"]
    if agent_id is None:
        agent_id = "default"
    agent_data = AGENT_REGISTRY[agent_id]
    agent = agent_data["instance"]
    try:
        response = await agent.run(state["input_text"], {})
        # Ensure response is a string
        if not isinstance(response, str):
            response = str(response)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error in agent {agent_id}: {e}")
        return {"response": f"Error: {str(e)}"}


def create_graph() -> Any:
    """Create and configure the LangGraph state graph.

    Returns
    -------
        A compiled LangGraph state graph for agent routing and execution

    """
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
