"""Tests for the weather agent module.

This module contains test cases for the WeatherAgent class, verifying its ability to
process weather-related queries and handle various input scenarios.
"""

import pytest

from agents.agent_weather import WeatherAgent


@pytest.fixture
def weather_agent() -> WeatherAgent:
    """Create a WeatherAgent instance for testing.

    Returns
    -------
        WeatherAgent: A configured instance of the weather agent for testing.

    """
    return WeatherAgent()


@pytest.mark.asyncio
async def test_weather_agent_basic_response(weather_agent: WeatherAgent) -> None:
    """Test that the weather agent returns a basic weather response.

    Args:
    ----
        weather_agent: The WeatherAgent instance to test.

    This test verifies that the agent can process a basic weather query and return
    a response containing expected weather information.

    """
    input_text = "What's the weather like today?"
    context = {"location": "New York"}

    response = await weather_agent.run(input_text, context)

    assert isinstance(response, str)
    assert "weather" in response.lower()
    assert "sunny" in response.lower()
    assert "25°C" in response


@pytest.mark.asyncio
async def test_weather_agent_empty_input(weather_agent: WeatherAgent) -> None:
    """Test that the weather agent handles empty input gracefully.

    Args:
    ----
        weather_agent: The WeatherAgent instance to test.

    This test ensures the agent can handle empty input without raising exceptions
    and returns a meaningful response.

    """
    input_text = ""
    context = {}

    response = await weather_agent.run(input_text, context)

    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_weather_agent_with_context(weather_agent: WeatherAgent) -> None:
    """Test that the weather agent processes context information correctly.

    Args:
    ----
        weather_agent: The WeatherAgent instance to test.

    This test verifies that the agent can process weather queries with additional
    context parameters like location, units, and time.

    """
    input_text = "What's the weather?"
    context = {"location": "London", "units": "metric", "time": "current"}

    response = await weather_agent.run(input_text, context)

    assert isinstance(response, str)
    assert "weather" in response.lower()
    assert "sunny" in response.lower()
    assert "25°C" in response
