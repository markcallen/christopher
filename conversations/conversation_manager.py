from .thread_store import save_message


async def handle_message(agent, thread_id: str, input_text: str):
    save_message(thread_id, "user", input_text)
    response = await agent.run(input_text, {})
    save_message(thread_id, agent.id, response)
    return response
