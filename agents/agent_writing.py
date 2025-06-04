from langchain_openai.chat_models.base import ChatOpenAI

from core.registry import agent


@agent("writing")
class WritingAgent:
    id = "writing"
    description = "A writing assistant that helps with content creation, editing, and writing tasks using GPT-4"

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)

    async def run(self, input_text: str, context: dict) -> str:
        response = await self.llm.ainvoke(input_text)
        return response.content
