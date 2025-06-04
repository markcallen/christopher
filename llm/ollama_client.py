import os
from langchain_ollama.llms import OllamaLLM
from pydantic import BaseModel


class OllamaClient:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3")
        self.llm = OllamaLLM(model=self.model, base_url=self.base_url)

    async def generate(self, prompt: str, format: BaseModel) -> str:
        return await self.llm.agenerate([prompt], format=format.model_json_schema())
