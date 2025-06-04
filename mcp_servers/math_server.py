class MathServer:
    id = "math"

    async def send_request(self, input_text: str) -> str:
        try:
            result = eval(input_text)
            return f"Result: {result}"
        except Exception:
            return "Error evaluating expression."
