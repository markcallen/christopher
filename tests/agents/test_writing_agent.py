"""Tests for the WritingAgent class."""

import os
from unittest.mock import AsyncMock, patch

import pytest


@pytest.fixture(autouse=True, scope="module")
def mock_openai_api_key():
    """Mock the OpenAI API key environment variable at module scope."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test-key"}, clear=True):
        yield


@pytest.fixture
def mock_llm():
    """Mock the ChatOpenAI LLM to simulate responses."""
    mock_instance = AsyncMock()
    mock_instance.ainvoke = AsyncMock()

    with patch(
        "agents.agent_writing.ChatOpenAI", return_value=mock_instance
    ) as mock_class:
        # Mock the initialization to accept any kwargs
        mock_class.return_value = mock_instance
        mock_class.side_effect = lambda **kwargs: mock_instance
        yield mock_instance


@pytest.fixture
def writing_agent(mock_llm):
    """Create a WritingAgent instance with mocked LLM."""
    from agents.agent_writing import WritingAgent  # Import here after mocking

    return WritingAgent()


@pytest.mark.asyncio
async def test_writing_agent_string_response(writing_agent, mock_llm):
    """Test WritingAgent with a string response from LLM."""
    mock_llm.ainvoke.return_value.content = "This is a test response"

    result = await writing_agent.run("Write a test", {})

    assert result == "This is a test response"
    mock_llm.ainvoke.assert_called_once_with("Write a test")


@pytest.mark.asyncio
async def test_writing_agent_list_response(writing_agent, mock_llm):
    """Test WritingAgent with a list response from LLM."""
    mock_llm.ainvoke.return_value.content = ["First", "Second", "Third"]

    result = await writing_agent.run("Write a list", {})

    assert result == "First Second Third"
    mock_llm.ainvoke.assert_called_once_with("Write a list")


@pytest.mark.asyncio
async def test_writing_agent_other_response(writing_agent, mock_llm):
    """Test WritingAgent with a non-string, non-list response from LLM."""
    mock_llm.ainvoke.return_value.content = {"key": "value"}

    result = await writing_agent.run("Write a dict", {})

    assert result == "{'key': 'value'}"
    mock_llm.ainvoke.assert_called_once_with("Write a dict")


@pytest.mark.asyncio
async def test_writing_agent_with_context(writing_agent, mock_llm):
    """Test WritingAgent with additional context."""
    mock_llm.ainvoke.return_value.content = "Context-aware response"
    context = {"style": "formal", "tone": "professional"}

    result = await writing_agent.run("Write with context", context)

    assert result == "Context-aware response"
    mock_llm.ainvoke.assert_called_once_with("Write with context")
