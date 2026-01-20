from graph.graph import ticket_agent

def run_agent(user_message: str, ticket_id: str | None = None):
    return ticket_agent.invoke({
        "user_message": user_message,
        "ticket_id": ticket_id
    })
