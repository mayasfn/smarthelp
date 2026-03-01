from backend.db.zen_repo import ZenRepository

def check_for_resolution(state: dict):
    ticket_id = state.get("ticket_id")
    # Check the flag returned by the merged generate_response node
    is_resolved = state.get("is_resolved", False)

    if ticket_id and is_resolved:
        repo = ZenRepository()
        # Update Snowflake status to CLOSED
        repo.session.sql(
            "UPDATE ZEN_TICKETS SET STATUS = 'CLOSED' WHERE TICKET_ID = ?",
            params=[ticket_id]
        ).collect()
        return {"status": "CLOSED"}
    
    return {}