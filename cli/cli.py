"""CLI for Christopher."""

import asyncio

import inquirer
from dotenv import load_dotenv

from core.christopher import load_agents, run_with_langgraph

# Load environment variables from .env file
load_dotenv()


async def main():
    """Run the main CLI loop."""
    load_agents()
    # thread_id = await inquirer.text("Thread ID (new or existing)")

    while True:
        user_input = inquirer.text(
            "You:"
        )  # Remove await since inquirer.text is not async
        if user_input.lower() in ["exit", "quit"]:
            break
        try:
            response = await run_with_langgraph(user_input)
            print(f"Christopher: {response}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
