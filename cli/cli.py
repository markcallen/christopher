import inquirer
import asyncio
from core.christopher import load_agents, run_with_langgraph
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


async def main():
    load_agents()
    # thread_id = await inquirer.text("Thread ID (new or existing)")

    while True:
        user_input = await inquirer.text("You:")
        if user_input.lower() in ["exit", "quit"]:
            break
        try:
            response = await run_with_langgraph(user_input)
            print(f"Christopher: {response}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
