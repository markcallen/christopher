"""Tests for the OllamaClient class.

This module contains test cases for the OllamaClient class, including initialization,
environment variable handling, and LLM generation functionality.
"""

import os
from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest
from langchain.schema import Generation, LLMResult
from pydantic import BaseModel

from llm.ollama_client import OllamaClient


class SampleFormat(BaseModel):
    """Test format for OllamaClient.generate."""

    name: str
    age: int


@pytest.fixture
def mock_env_vars() -> Generator[None, None, None]:
    """Fixture to set test environment variables."""
    with patch.dict(
        os.environ,
        {"OLLAMA_BASE_URL": "http://test-url:11434", "OLLAMA_MODEL": "test-model"},
    ):
        yield


@pytest.fixture
def mock_llm() -> Generator[AsyncMock, None, None]:
    """Fixture to mock OllamaLLM."""
    with patch("llm.ollama_client.OllamaLLM") as mock:
        mock_instance = mock.return_value
        mock_instance.agenerate = AsyncMock()
        yield mock_instance


@pytest.fixture
def client(mock_env_vars: None, mock_llm: AsyncMock) -> OllamaClient:
    """Fixture to create OllamaClient instance with mocked dependencies."""
    return OllamaClient()


def test_init_default_values() -> None:
    """Test initialization with default values (no env vars)."""
    with patch.dict(os.environ, {}, clear=True):
        client = OllamaClient()
        assert client.base_url == "http://localhost:11434"
        assert client.model == "llama3"


def test_init_custom_values(mock_env_vars: None) -> None:
    """Test initialization with custom environment variables."""
    client = OllamaClient()
    assert client.base_url == "http://test-url:11434"
    assert client.model == "test-model"


@pytest.mark.asyncio
async def test_generate(client: OllamaClient, mock_llm: AsyncMock) -> None:
    """Test the generate method."""
    # Setup test data
    test_prompt = "Test prompt"
    test_format = SampleFormat(name="test", age=25)
    expected_result = LLMResult(
        generations=[[Generation(text='{"name": "test", "age": 25}')]]
    )
    mock_llm.agenerate.return_value = expected_result

    # Call the method
    result = await client.generate(test_prompt, test_format)

    # Verify the result
    assert result == expected_result
    mock_llm.agenerate.assert_called_once_with(
        [test_prompt], format=test_format.model_json_schema()
    )


@pytest.mark.asyncio
async def test_generate_with_invalid_format(
    client: OllamaClient, mock_llm: AsyncMock
) -> None:
    """Test generate method with an invalid format."""

    class InvalidFormat(BaseModel):
        """Invalid format for testing error handling."""

        invalid_field: dict  # Invalid type for LLM output

    test_prompt = "Test prompt"
    test_format = InvalidFormat(invalid_field={})

    with pytest.raises(ValueError, match="Invalid format"):
        await client.generate(test_prompt, test_format)


@pytest.mark.asyncio
async def test_generate_llm_error(client: OllamaClient, mock_llm: AsyncMock) -> None:
    """Test generate method when LLM raises an error."""
    test_prompt = "Test prompt"
    test_format = SampleFormat(name="test", age=25)
    mock_llm.agenerate.side_effect = Exception("LLM service error")

    with pytest.raises(Exception, match="LLM service error"):
        await client.generate(test_prompt, test_format)


@pytest.mark.asyncio
async def test_generate_empty_prompt(client: OllamaClient, mock_llm: AsyncMock) -> None:
    """Test generate method with an empty prompt."""
    test_prompt = ""
    test_format = SampleFormat(name="test", age=25)
    expected_result = LLMResult(
        generations=[[Generation(text='{"name": "test", "age": 25}')]]
    )
    mock_llm.agenerate.return_value = expected_result

    result = await client.generate(test_prompt, test_format)
    assert result == expected_result
    mock_llm.agenerate.assert_called_once_with(
        [test_prompt], format=test_format.model_json_schema()
    )


def test_init_invalid_url() -> None:
    """Test initialization with an invalid URL."""
    with patch.dict(os.environ, {"OLLAMA_BASE_URL": "invalid-url"}):
        with pytest.raises(ValueError, match="Invalid URL"):
            OllamaClient()
