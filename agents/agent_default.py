"""A default agent that handles general queries and tasks."""

from langchain_openai.chat_models.base import ChatOpenAI

from core.registry import agent


@agent("default")
class DefaultAgent:
    """A default agent that handles general queries and tasks."""

    id = "default"
    description = "A default agent that handles general queries and tasks"

    def __init__(self):
        """Initialize the default agent."""
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    async def run(self, input_text: str, context: dict) -> str:
        """Process the input text and return a response.

        Args:
        ----
            input_text: The text input from the user
            context: Additional context information

        Returns:
        -------
            A string response

        """
        response = await self.llm.ainvoke(input_text)
        return response.content
