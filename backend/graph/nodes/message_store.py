from graph.state import ZenState
from db.zen_repo import ZenRepository

def store_agent_message(state: ZenState) -> dict:
    repo = ZenRepository()

    repo.add_message(
        ticket_id=state["ticket_id"],
        role="AGENT_AI",
        content=state["response"]
    )

    return {}
