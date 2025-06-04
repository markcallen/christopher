"""A math agent that can perform calculations and solve mathematical expressions."""

from core.registry import agent
from mcp_servers.math_server import MathServer


@agent("math")
class MathAgent:
    """A math agent that can perform calculations and solve mathematical expressions."""

    id = "math"
    description = (
        "A math agent that can perform calculations and solve "
        "mathematical expressions"
    )

    async def run(self, input_text: str, context: dict) -> str:
        """Run the math agent on the input text."""
        server = MathServer()
        return await server.send_request(input_text)
