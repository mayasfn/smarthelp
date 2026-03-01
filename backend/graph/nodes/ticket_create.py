from ..state import ZenState
from ...db.zen_repo import ZenRepository

def create_ticket(state: ZenState) -> dict:
    repo = ZenRepository()

    ticket_id = repo.create_ticket(
        subject=state["user_message"][:100],
        priority=state["priority"]
    )

    repo.add_message(
        ticket_id=ticket_id,
        role="USER",
        content=state["user_message"]
    )

    return {"ticket_id": ticket_id}
