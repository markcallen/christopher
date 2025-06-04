"""Tests for the programming agent module.

This module contains test cases for the ProgrammingAgent class, verifying its
ability to process programming-related queries and handle various input scenarios.
"""

from collections.abc import Generator
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from agents.agent_programming import ProgrammingAgent


@pytest.fixture
def mock_chat_anthropic() -> Generator[AsyncMock, None, None]:
    """Mock the ChatAnthropic model to simulate responses."""
    with patch("agents.agent_programming.ChatAnthropic") as mock:
        mock_instance = AsyncMock()
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def programming_agent(mock_chat_anthropic: AsyncMock) -> ProgrammingAgent:
    """Create a ProgrammingAgent instance with mocked dependencies."""
    return ProgrammingAgent()


@pytest.mark.asyncio
async def test_programming_agent_initialization() -> None:
    """Test that the ProgrammingAgent initializes correctly."""
    agent = ProgrammingAgent()
    assert agent.id == "programming"
    assert isinstance(agent.description, str)
    assert agent.llm is not None


@pytest.mark.asyncio
async def test_programming_agent_run_string_response(
    programming_agent: ProgrammingAgent,
    mock_chat_anthropic: AsyncMock,
) -> None:
    """Test the run method with a string response."""
    # Setup
    test_input = "Write a hello world function"
    test_context: dict[str, Any] = {"language": "python"}
    expected_response = "def hello_world():\n    print('Hello, World!')"

    mock_chat_anthropic.ainvoke.return_value.content = expected_response

    # Execute
    response = await programming_agent.run(test_input, test_context)

    # Verify
    assert response == expected_response
    mock_chat_anthropic.ainvoke.assert_called_once_with(test_input)


@pytest.mark.asyncio
async def test_programming_agent_run_list_response(
    programming_agent: ProgrammingAgent,
    mock_chat_anthropic: AsyncMock,
) -> None:
    """Test the run method with a list response that gets converted to string."""
    # Setup
    test_input = "List programming languages"
    test_context: dict[str, Any] = {}
    list_response = ["Python", "JavaScript", "Rust"]

    mock_chat_anthropic.ainvoke.return_value.content = list_response

    # Execute
    response = await programming_agent.run(test_input, test_context)

    # Verify
    assert response == str(list_response)
    mock_chat_anthropic.ainvoke.assert_called_once_with(test_input)


@pytest.mark.asyncio
async def test_programming_agent_run_error_handling(
    programming_agent: ProgrammingAgent,
    mock_chat_anthropic: AsyncMock,
) -> None:
    """Test that the agent handles errors gracefully."""
    # Setup
    test_input = "Invalid request"
    test_context: dict[str, Any] = {}
    mock_chat_anthropic.ainvoke.side_effect = Exception("API Error")

    # Execute and verify
    with pytest.raises(Exception) as exc_info:
        await programming_agent.run(test_input, test_context)

    assert str(exc_info.value) == "API Error"
    mock_chat_anthropic.ainvoke.assert_called_once_with(test_input)
