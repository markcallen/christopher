"""A programming assistant that helps with coding tasks, debugging, and software."""

from typing import Any

from langchain_anthropic.chat_models import ChatAnthropic
from langchain_mcp_adapters.client import MultiServerMCPClient

from core.registry import agent


@agent("programming")
class ProgrammingAgent:
    """A programming assistant that helps with coding tasks, debugging, and software."""

    id = "programming"
    description = (
        "A programming assistant that helps with coding tasks, "
        "debugging, and software development.  Including tools for "
        "GitHub and Jira."
    )

    def __init__(self) -> None:
        """Initialize the programming agent."""
        self.llm: ChatAnthropic | None = None
        self.client: MultiServerMCPClient | None = None

    async def initialize(self) -> None:
        """Async initialization of the programming agent with Claude model."""
        self.client = MultiServerMCPClient(
            {
                "github": {
                    "command": "docker",
                    "args": [
                        "run",
                        "-i",
                        "--rm",
                        "-e",
                        "GITHUB_PERSONAL_ACCESS_TOKEN",
                        "ghcr.io/github/github-mcp-server",
                    ],
                    "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": ""},
                },
                "mcp-atlassian": {
                    "command": "docker",
                    "args": [
                        "run",
                        "-i",
                        "--rm",
                        "-e",
                        "CONFLUENCE_URL",
                        "-e",
                        "CONFLUENCE_USERNAME",
                        "-e",
                        "CONFLUENCE_API_TOKEN",
                        "-e",
                        "JIRA_URL",
                        "-e",
                        "JIRA_USERNAME",
                        "-e",
                        "JIRA_API_TOKEN",
                        "ghcr.io/sooperset/mcp-atlassian:latest",
                    ],
                    "env": {
                        "CONFLUENCE_URL": "https://your-company.atlassian.net/wiki",
                        "CONFLUENCE_USERNAME": "your.email@company.com",
                        "CONFLUENCE_API_TOKEN": "your_confluence_api_token",
                        "JIRA_URL": "https://your-company.atlassian.net",
                        "JIRA_USERNAME": "your.email@company.com",
                        "JIRA_API_TOKEN": "your_jira_api_token",
                    },
                },
            }
        )
        tools = await self.client.get_tools()
        self.llm = ChatAnthropic(
            model_name="claude-3-opus-20240229",
            temperature=0,
            timeout=60,
            stop=None,
            tools=tools,
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
        if not self.llm:
            await self.initialize()
        assert self.llm is not None  # For type checker
        response = await self.llm.ainvoke(input_text)
        if isinstance(response.content, str):
            return response.content
        return str(response.content)
