from backend.db.zen_repo import ZenRepository
from backend.graph.state import ZenState

def check_for_resolution(state: ZenState):
    ticket_id = state.get("ticket_id")
    is_resolved = state.get("is_resolved", False)

    if ticket_id and is_resolved:
        repo = ZenRepository()
        repo.close_ticket(ticket_id)
        return {}
    
    return {}