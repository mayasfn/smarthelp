import os

from backend.graph.state import ZenState
from backend.db.zen_repo import ZenRepository

def create_ticket(state: ZenState) -> dict:
    repo = ZenRepository()

    ticket_id = repo.create_ticket(
        user=os.getenv("SNOWFLAKE_USER"), ## To change based on auth implementation in a prod setting
        subject=state.get("subject", state["user_message"][:50]),
        priority=state["priority"],
        type=state.get("type", "Request"),
        queue=state.get("queue", "General Inquiry")
    )

    repo.add_message(
        ticket_id=ticket_id,
        role="USER",
        content=state["user_message"]
    )

    return {"ticket_id": ticket_id}
