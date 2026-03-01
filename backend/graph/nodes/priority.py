from backend.graph.state import ZenState
from backend.llm.model import llm
from langchain_core.messages import HumanMessage

def evaluate_priority(state: ZenState) -> dict:
    msg = HumanMessage(
        content=f"Classify priority: {state['user_message']}"
    )

    raw = llm.invoke([msg]).content.upper()

    if "URGENT" in raw:
        priority = "URGENT"
    elif "HIGH" in raw:
        priority = "HIGH"
    elif "MED" in raw:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    return {"priority": priority}
