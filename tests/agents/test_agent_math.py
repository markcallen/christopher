"""Tests for the MathAgent class."""

from unittest.mock import AsyncMock, patch

import pytest

from agents.agent_math import MathAgent


@pytest.fixture
def mock_math_server():
    """Mock the MathServer to simulate math calculations."""
    with patch("agents.agent_math.MathServer") as mock:
        mock_instance = AsyncMock()
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def math_agent():
    """Create a MathAgent instance for testing."""
    return MathAgent()


@pytest.mark.asyncio
async def test_math_agent_basic_calculation(math_agent, mock_math_server):
    """Test that the math agent can perform basic calculations."""
    # Setup
    mock_math_server.send_request.return_value = "42"
    input_text = "2 + 40"
    context = {}

    # Execute
    result = await math_agent.run(input_text, context)

    # Verify
    assert result == "42"
    mock_math_server.send_request.assert_called_once_with(input_text)


@pytest.mark.asyncio
async def test_math_agent_error_handling(math_agent, mock_math_server):
    """Test that the math agent handles errors gracefully."""
    # Setup
    mock_math_server.send_request.side_effect = Exception("Invalid expression")
    input_text = "invalid expression"
    context = {}

    # Execute and verify
    with pytest.raises(Exception) as exc_info:
        await math_agent.run(input_text, context)

    assert str(exc_info.value) == "Invalid expression"
    mock_math_server.send_request.assert_called_once_with(input_text)


@pytest.mark.asyncio
async def test_math_agent_complex_expression(math_agent, mock_math_server):
    """Test that the math agent can handle complex mathematical expressions."""
    # Setup
    mock_math_server.send_request.return_value = "3.14159"
    input_text = "sin(pi/2)"
    context = {}

    # Execute
    result = await math_agent.run(input_text, context)

    # Verify
    assert result == "3.14159"
    mock_math_server.send_request.assert_called_once_with(input_text)
