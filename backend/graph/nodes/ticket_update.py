from backend.graph.state import ZenState
from backend.db.zen_repo import ZenRepository

def update_ticket(state: ZenState) -> dict:
    repo = ZenRepository()

    repo.add_message(
        ticket_id=state["ticket_id"],
        role="USER",
        content=state["user_message"]
    )

    return {}
