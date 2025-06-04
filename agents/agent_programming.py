"""A programming assistant that helps with coding tasks, debugging, and software."""

from typing import Any

from langchain_anthropic.chat_models import ChatAnthropic

from core.registry import agent


@agent("programming")
class ProgrammingAgent:
    """A programming assistant that helps with coding tasks, debugging, and software."""

    id = "programming"
    description = (
        "A programming assistant that helps with coding tasks, "
        "debugging, and software development"
    )

    def __init__(self) -> None:
        """Initialize the programming agent with Claude model."""
        self.llm = ChatAnthropic(
            model_name="claude-3-opus-20240229",
            temperature=0,
            timeout=60,
            stop=None,
        )

    async def run(self, input_text: str, context: dict[str, Any]) -> str:
        """Run the programming agent on the input text.

        Args:
        ----
            input_text: The input text to process
            context: Additional context for the agent

        Returns:
        -------
            The agent's response as a string

        """
        response = await self.llm.ainvoke(input_text)
        if isinstance(response.content, str):
            return response.content
        return str(response.content)
