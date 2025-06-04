"""A writing assistant that helps with content creation, editing, and writing tasks."""

from typing import Any

from langchain_openai.chat_models.base import ChatOpenAI

from core.registry import agent


@agent("writing")
class WritingAgent:
    """A writing assistant that helps with content creation."""

    id = "writing"
    description = (
        "A writing assistant that helps with content creation, editing, "
        "and writing tasks using GPT-4"
    )

    def __init__(self) -> None:
        """Initialize the writing agent with GPT-4 model."""
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)

    async def run(self, input_text: str, context: dict[str, Any]) -> str:
        """Process the input text and return a response.

        Args:
        ----
            input_text: The text input to process
            context: Additional context for processing

        Returns:
        -------
            The processed text response as a string

        """
        response = await self.llm.ainvoke(input_text)
        if isinstance(response.content, str):
            return response.content
        if isinstance(response.content, list):
            # Join list items into a single string
            return " ".join(str(item) for item in response.content)
        return str(response.content)
