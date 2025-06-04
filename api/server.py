from fastapi import FastAPI
from pydantic import BaseModel
from core.christopher import load_agents, run_with_langgraph
from conversations.thread_store import list_threads, get_thread

app = FastAPI()
load_agents()


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(req: ChatRequest):
    response = await run_with_langgraph(req.message)
    return {"response": response}


@app.get("/threads")
def threads():
    return {"threads": list_threads()}


@app.get("/thread/{thread_id}")
def thread(thread_id: str):
    return {"messages": get_thread(thread_id)}
