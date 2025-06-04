"""Client for interacting with Ollama LLM models."""

import os
from urllib.parse import urlparse

from langchain.schema import LLMResult
from langchain_ollama.llms import OllamaLLM
from pydantic import BaseModel


class OllamaClient:
    """Client for interacting with Ollama LLM models.

    This client provides a wrapper around the Ollama LLM service, handling
    configuration and providing a simple interface for generating text.
    """

    def __init__(self) -> None:
        """Initialize the Ollama client.

        Sets up the base URL and model name from environment variables,
        with fallback defaults. Validates the URL format.

        Raises
        ------
            ValueError: If the base URL is invalid.

        """
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

    async def generate(
        self, prompt: str, format: type[BaseModel] | BaseModel
    ) -> LLMResult:
        """Generate text using the Ollama model.

        Args:
        ----
            prompt: The input prompt to generate text from.
            format: A Pydantic model class or instance defining the expected
            output format.

        Returns:
        -------
            LLMResult containing the generated text.

        Raises:
        ------
            ValueError: If the format contains non-serializable fields.

        """
        return await self.llm.agenerate([prompt], format=format.model_json_schema())
