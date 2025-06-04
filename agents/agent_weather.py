from core.registry import agent


@agent("weather")
class WeatherAgent:
    id = "weather"
    description = (
        "A weather agent that provides current weather information and forecasts"
    )

    async def run(self, input_text: str, context: dict) -> str:
        return "The weather today is sunny with a high of 25°C."
