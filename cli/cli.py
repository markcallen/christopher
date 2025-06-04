import inquirer
import asyncio
from core.christopher import load_agents, run_with_langgraph
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


async def main():
    load_agents()
    # thread_id = inquirer.text("Thread ID (new or existing)")

    while True:
        user_input = inquirer.text("You:")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = await run_with_langgraph(user_input)
        print(f"Christopher: {response}")


if __name__ == "__main__":
    asyncio.run(main())
