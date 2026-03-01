from backend.graph.state import ZenState

def route_ticket(state: ZenState) -> str:
    if state.get("ticket_id") is None:
        return "new_ticket"
    return "existing_ticket"
