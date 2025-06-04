"""Tests for the DefaultAgent class."""

import os
from unittest.mock import AsyncMock, patch

import pytest
from langchain_openai.chat_models.base import ChatOpenAI


@pytest.fixture(autouse=True)
def mock_openai_api_key():
    """Mock OPENAI_API_KEY environment variable for all tests."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "dummy-key"}):
        yield


@pytest.fixture
def mock_llm():
    """Mock the ChatOpenAI instance to control LLM responses."""
    with patch("agents.agent_default.ChatOpenAI") as mock:
        mock_instance = AsyncMock()
        mock_instance.ainvoke = AsyncMock()
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def default_agent(mock_llm):
    """Create a DefaultAgent instance with mocked LLM."""
    from agents.agent_default import DefaultAgent

    return DefaultAgent()


@pytest.mark.asyncio
async def test_default_agent_initialization():
    """Test that DefaultAgent initializes with correct attributes."""
    from agents.agent_default import DefaultAgent

    agent = DefaultAgent()
    assert agent.id == "default"
    assert agent.description == "A default agent that handles general queries and tasks"
    assert isinstance(agent.llm, ChatOpenAI)


@pytest.mark.asyncio
async def test_default_agent_run_success(default_agent, mock_llm):
    """Test successful execution of the run method."""
    # Setup
    test_input = "Hello, how are you?"
    test_context = {"some": "context"}
    expected_response = "I'm doing well, thank you!"
    mock_llm.ainvoke.return_value.content = expected_response

    # Execute
    response = await default_agent.run(test_input, test_context)

    # Verify
    assert response == expected_response
    mock_llm.ainvoke.assert_called_once_with(test_input)


@pytest.mark.asyncio
async def test_default_agent_run_with_empty_input(default_agent, mock_llm):
    """Test run method with empty input."""
    # Setup
    test_input = ""
    test_context = {}
    expected_response = "I received an empty message."
    mock_llm.ainvoke.return_value.content = expected_response

    # Execute
    response = await default_agent.run(test_input, test_context)

    # Verify
    assert response == expected_response
    mock_llm.ainvoke.assert_called_once_with(test_input)


@pytest.mark.asyncio
async def test_default_agent_run_with_long_input(default_agent, mock_llm):
    """Test run method with a long input string."""
    # Setup
    test_input = "This is a very long input string " * 10
    test_context = {}
    expected_response = "I processed your long message."
    mock_llm.ainvoke.return_value.content = expected_response

    # Execute
    response = await default_agent.run(test_input, test_context)

    # Verify
    assert response == expected_response
    mock_llm.ainvoke.assert_called_once_with(test_input)
