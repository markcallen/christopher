"""API for the Christopher chatbot."""

from fastapi import FastAPI
from pydantic import BaseModel

from conversations.thread_store import get_thread, list_threads
from core.christopher import load_agents, run_with_langgraph

app = FastAPI()
load_agents()


class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""

    message: str


@app.post("/chat")
async def chat(req: ChatRequest):
    """Chat endpoint."""
    response = await run_with_langgraph(req.message)
    return {"response": response}


@app.get("/threads")
def threads():
    """Threads endpoint."""
    return {"threads": list_threads()}


@app.get("/thread/{thread_id}")
def thread(thread_id: str):
    """Thread endpoint."""
    return {"messages": get_thread(thread_id)}
