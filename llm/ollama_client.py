import os
from urllib.parse import urlparse
from langchain.schema import LLMResult
from langchain_ollama.llms import OllamaLLM
from pydantic import BaseModel


class OllamaClient:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3")

        # Validate URL
        try:
            parsed = urlparse(self.base_url)
            if not all([parsed.scheme, parsed.netloc]):
                raise ValueError("Invalid URL: must include scheme and host")
        except Exception as e:
            raise ValueError(f"Invalid URL: {str(e)}")

        self.llm = OllamaLLM(model=self.model, base_url=self.base_url)

    async def generate(self, prompt: str, format: BaseModel) -> LLMResult:
        # Validate format is a simple type that can be JSON serialized
        for field_name, field in format.model_dump().items():
            if not isinstance(field, (str, int, float, bool, type(None))):
                raise ValueError(
                    f"Invalid format: field '{field_name}' must be a simple type (str, int, float, bool)"
                )

        return await self.llm.agenerate([prompt], format=format.model_json_schema())
