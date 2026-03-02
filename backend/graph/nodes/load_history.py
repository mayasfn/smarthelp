
from backend.graph.state import ZenState
from backend.db.zen_repo import ZenRepository

def load_ticket_history(state: ZenState) -> dict:
    ticket_id = state.get("ticket_id")
    if not ticket_id:
        return {"messages": []}
        
    repo = ZenRepository()
    history = repo.get_ticket_messages(ticket_id) 
    return {"messages": history}