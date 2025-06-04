"""CLI for Christopher."""

import asyncio
import logging

import inquirer
from dotenv import load_dotenv

from core.christopher import load_agents, run_with_langgraph

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


async def main():
    """Run the main CLI loop."""
    logger.info("Starting Christopher CLI")
    load_agents()
    logger.info("Agents loaded successfully")
    # thread_id = await inquirer.text("Thread ID (new or existing)")

    while True:
        user_input = inquirer.text(
            "You:"
        )  # Remove await since inquirer.text is not async
        logger.info(f"User input: {user_input}")

        if user_input.lower() in ["exit", "quit"]:
            logger.info("User requested exit")
            break

        try:
            logger.info("Processing user input with langgraph")
            response = await run_with_langgraph(user_input)
            logger.info(f"Generated response: {response}")
            print(f"Christopher: {response}")  # noqa: T201
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}", exc_info=True)
            logger.error(f"Error: {e}")

    logger.info("Christopher CLI session ended")


if __name__ == "__main__":
    asyncio.run(main())
