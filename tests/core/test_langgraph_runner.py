"""Tests for the langgraph_runner module."""

from unittest.mock import AsyncMock, patch

import pytest
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, LLMResult

from core.langgraph_runner import (
    AgentResponseFormatter,
    ChatState,
    ChatStateDict,
    agent_node,
    create_graph,
    entry_node,
)


@pytest.fixture
def mock_ollama():
    """Mock the Ollama client for testing."""
    with patch("core.langgraph_runner.OllamaClient") as mock:
        mock_instance = AsyncMock()
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_agent():
    """Mock an agent for testing."""
    agent = AsyncMock()
    agent.run.return_value = "Test response"
    return agent


@pytest.fixture
def mock_agent_registry(mock_agent):
    """Mock the agent registry for testing."""
    with patch("core.langgraph_runner.AGENT_REGISTRY") as mock:
        mock_registry = {
            "default": {"instance": mock_agent, "description": "Default agent"},
            "test": {"instance": mock_agent, "description": "Test agent"},
        }
        mock.__getitem__.side_effect = mock_registry.__getitem__
        mock.__contains__.side_effect = mock_registry.__contains__
        mock.keys.return_value = mock_registry.keys()
        yield mock_registry


@pytest.mark.asyncio
async def test_entry_node_routes_to_default_agent(mock_ollama, mock_agent_registry):
    """Test that entry_node routes to default agent when no specific agent is needed."""
    # Setup
    state: ChatStateDict = {
        "input_text": "Hello",
        "agent_id": None,
        "response": "",
    }
    mock_ollama.generate.return_value = None  # Simulate non-LLMResult response

    # Execute
    result = await entry_node(state)

    # Verify
    assert result == {"agent_id": "default"}
    mock_ollama.generate.assert_called_once()


@pytest.mark.asyncio
async def test_entry_node_routes_to_specific_agent(mock_ollama, mock_agent_registry):
    """Test that entry_node routes to a specific agent when requested."""
    # Setup
    state: ChatStateDict = {
        "input_text": "Hello",
        "agent_id": None,
        "response": "",
    }
    # Create a proper LLMResult with a ChatGeneration
    message = AIMessage(content='{"id": "test"}')
    generation = ChatGeneration(message=message)
    mock_response = LLMResult(generations=[[generation]])
    mock_ollama.generate.return_value = mock_response

    # Execute
    result = await entry_node(state)

    # Verify
    assert result == {"agent_id": "test"}
    mock_ollama.generate.assert_called_once()


@pytest.mark.asyncio
async def test_entry_node_handles_unknown_agent(mock_ollama, mock_agent_registry):
    """Test that entry_node routes to default agent when unknown agent is requested."""
    # Setup
    state: ChatStateDict = {
        "input_text": "Hello",
        "agent_id": None,
        "response": "",
    }
    # Create a proper LLMResult with a ChatGeneration
    message = AIMessage(content='{"id": "unknown"}')
    generation = ChatGeneration(message=message)
    mock_response = LLMResult(generations=[[generation]])
    mock_ollama.generate.return_value = mock_response

    # Execute
    result = await entry_node(state)

    # Verify
    assert result == {"agent_id": "default"}
    mock_ollama.generate.assert_called_once()


@pytest.mark.asyncio
async def test_agent_node_processes_input(mock_agent_registry):
    """Test that agent_node processes input and returns response."""
    # Setup
    state: ChatStateDict = {
        "input_text": "Hello",
        "agent_id": "test",
        "response": "",
    }

    # Execute
    result = await agent_node(state)

    # Verify
    assert result == {"response": "Test response"}
    mock_agent_registry["test"]["instance"].run.assert_called_once_with("Hello", {})


@pytest.mark.asyncio
async def test_agent_node_handles_none_agent_id(mock_agent_registry):
    """Test that agent_node defaults to default agent when agent_id is None."""
    # Setup
    state: ChatStateDict = {
        "input_text": "Hello",
        "agent_id": None,
        "response": "",
    }

    # Execute
    result = await agent_node(state)

    # Verify
    assert result == {"response": "Test response"}
    mock_agent_registry["default"]["instance"].run.assert_called_once_with("Hello", {})


def test_create_graph_creates_valid_graph(mock_agent_registry):
    """Test that create_graph creates a valid graph."""
    # Execute
    graph = create_graph()

    # Verify
    assert graph is not None
    # Note: We can't easily verify the internal structure of the graph
    # as it's a compiled object, but we can verify it was created successfully


@pytest.mark.asyncio
async def test_chat_state_initialization():
    """Test that ChatState initializes correctly."""
    # Execute
    state = ChatState("Hello", "test")

    # Verify
    assert state.input_text == "Hello"
    assert state.agent_id == "test"
    assert state.response == ""


@pytest.mark.asyncio
async def test_agent_response_formatter():
    """Test that AgentResponseFormatter validates input correctly."""
    # Test valid initialization
    formatter = AgentResponseFormatter(id="test")
    assert formatter.id == "test"

    # Test validation - None is not allowed
    with pytest.raises(ValueError):
        AgentResponseFormatter(id=None)  # type: ignore
