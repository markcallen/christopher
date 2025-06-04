from core.registry import agent
from mcp_servers.math_server import MathServer


@agent("math")
class MathAgent:
    id = "math"
    description = "A mathematical agent that can perform calculations and solve mathematical expressions"

    async def run(self, input_text: str, context: dict) -> str:
        server = MathServer()
        return await server.send_request(input_text)
