def route_ticket(state: ZendeskState) -> str:
    if state.get("ticket_id") is None:
        return "new_ticket"
    return "existing_ticket"
