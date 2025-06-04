from langchain_anthropic.chat_models import ChatAnthropic

from core.registry import agent


@agent("programming")
class ProgrammingAgent:
    id = "programming"
    description = "A programming assistant that helps with coding tasks, debugging, and software development using Claude"

    def __init__(self):
        self.llm = ChatAnthropic(model="claude-3-opus-20240229", temperature=0)

    async def run(self, input_text: str, context: dict) -> str:
        response = await self.llm.ainvoke(input_text)
        return response.content
