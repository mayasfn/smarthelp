from typing import Optional

from graph.graph import ticket_agent


def run_agent(user_message: str, ticket_id: Optional[str] = None):
    return ticket_agent.invoke({
        "user_message": user_message,
        "ticket_id": ticket_id
    })
