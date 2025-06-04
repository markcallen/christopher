"""Weather agent module for providing weather information and forecasts."""

from core.registry import agent


@agent("weather")
class WeatherAgent:
    """Agent that provides current weather information and forecasts.

    This agent handles weather-related queries and returns formatted weather
    information including current conditions and forecasts.
    """

    id: str = "weather"
    description: str = (
        "A weather agent that provides current weather information and forecasts"
    )

    async def run(self, input_text: str, context: dict[str, str]) -> str:
        """Process weather-related queries and return weather information.

        Args:
        ----
            input_text: The user's input text containing the weather query
            context: Additional context information for processing the query

        Returns:
        -------
            A string containing the weather information response

        """
        return "The weather today is sunny with a high of 25°C."
