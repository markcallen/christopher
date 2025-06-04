"""Tests for the christopher module.

This module contains test cases for the core christopher functionality including
agent loading, retrieval, and LangGraph conversation execution.
"""

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from core.christopher import get_agent, load_agents, run_with_langgraph
from core.registry import AGENT_REGISTRY


@pytest.fixture
def mock_importlib() -> Generator[MagicMock, None, None]:
    """Mock the importlib module for testing module loading.

    Returns
    -------
        Generator yielding a mocked importlib.util module.

    """
    with patch("core.christopher.importlib.util") as mock:
        mock.spec_from_file_location.return_value = MagicMock(
            loader=MagicMock(exec_module=MagicMock())
        )
        yield mock


@pytest.fixture
def mock_os() -> Generator[MagicMock, None, None]:
    """Mock the os module for testing file operations.

    Returns
    -------
        Generator yielding a mocked os module with predefined path operations.

    """
    with patch("core.christopher.os") as mock:
        mock.path.join.return_value = "/fake/path/agent.py"
        mock.listdir.return_value = ["test_agent.py"]
        mock.path.dirname.return_value = "/fake/path"
        yield mock


@pytest.fixture
def mock_graph() -> Generator[MagicMock, None, None]:
    """Mock the LangGraph graph for testing run_with_langgraph.

    Returns
    -------
        Generator yielding a mocked graph instance with predefined behavior.

    """
    with patch("core.christopher.create_graph") as mock:
        graph_instance = MagicMock()
        graph_instance.get_graph.return_value = MagicMock(draw_mermaid_png=MagicMock())
        graph_instance.ainvoke = AsyncMock(return_value={"response": "Test response"})
        mock.return_value = graph_instance
        yield mock


@pytest.mark.asyncio
async def test_load_agents(
    mock_importlib: MagicMock,
    mock_os: MagicMock,
) -> None:
    """Test that load_agents successfully loads agent modules.

    Args:
    ----
        mock_importlib: Mocked importlib module
        mock_os: Mocked os module

    """
    # Call the function
    load_agents()

    # Verify the interactions
    # First call is for agents directory, second call is for filepath
    assert mock_os.path.join.call_count == 2
    mock_os.path.join.assert_any_call("/fake/path", "..", "agents")
    mock_os.path.join.assert_any_call(mock_os.path.join.return_value, "test_agent.py")

    mock_importlib.spec_from_file_location.assert_called_once_with(
        "test_agent", "/fake/path/agent.py"
    )
    mock_importlib.module_from_spec.assert_called_once()
    mock_importlib.spec_from_file_location.return_value.loader.exec_module.assert_called_once()


def test_get_agent_existing() -> None:
    """Test getting an existing agent from the registry.

    Verifies that get_agent returns the correct agent instance when the agent
    exists in the registry.
    """
    # Setup test data
    test_agent_instance = MagicMock()
    AGENT_REGISTRY["test_agent"] = {"instance": test_agent_instance}

    # Call the function
    result = get_agent("test_agent")

    # Verify the result
    assert result == test_agent_instance

    # Cleanup
    AGENT_REGISTRY.pop("test_agent")


def test_get_agent_nonexistent() -> None:
    """Test getting a non-existent agent from the registry.

    Verifies that get_agent returns None when the requested agent is not
    found in the registry.
    """
    # Call the function with non-existent agent
    result = get_agent("nonexistent_agent")

    # Verify the result
    assert result is None


@pytest.mark.asyncio
async def test_run_with_langgraph(mock_graph: MagicMock) -> None:
    """Test running a conversation with LangGraph.

    Args:
    ----
        mock_graph: Mocked LangGraph instance

    Verifies that the graph is properly configured and invoked with the
    correct input parameters.

    """
    # Call the function
    result = await run_with_langgraph("Hello")

    # Verify the interactions and result
    mock_graph.return_value.get_graph.assert_called_once()
    mock_graph.return_value.get_graph.return_value.draw_mermaid_png.assert_called_once_with(
        output_file_path="graph.png"
    )

    # Create a ChatState instance to match the implementation
    expected_state = {
        "input_text": "Hello",
        "agent_id": None,
        "response": "",
    }
    mock_graph.return_value.ainvoke.assert_called_once_with(expected_state)
    assert result == "Test response"


@pytest.mark.asyncio
async def test_run_with_langgraph_error(mock_graph: MagicMock) -> None:
    """Test error handling in run_with_langgraph.

    Args:
    ----
        mock_graph: Mocked LangGraph instance

    Verifies that exceptions from the graph invocation are properly
    propagated to the caller.

    """
    # Setup mock to raise an exception
    mock_graph.return_value.ainvoke.side_effect = Exception("Test error")

    # Verify that the error is propagated
    with pytest.raises(Exception) as exc_info:
        await run_with_langgraph("Hello")
    assert str(exc_info.value) == "Test error"
