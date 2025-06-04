import os
import importlib.util
from core.registry import AGENT_REGISTRY
from core.langgraph_runner import create_graph, ChatState


def load_agents():
    agents_dir = os.path.join(os.path.dirname(__file__), "..", "agents")
    for filename in os.listdir(agents_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            filepath = os.path.join(agents_dir, filename)
            spec = importlib.util.spec_from_file_location(filename[:-3], filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)


def get_agent(agent_id: str):
    agent_data = AGENT_REGISTRY.get(agent_id)
    return agent_data["instance"] if agent_data else None


async def run_with_langgraph(user_input: str):
    graph = create_graph()
    graph.get_graph().draw_mermaid_png(output_file_path="graph.png")
    state = ChatState(user_input)
    final_state = await graph.ainvoke(
        {
            "input_text": state.input_text,
            "agent_id": state.agent_id,
            "response": state.response,
        }
    )
    return final_state["response"]
