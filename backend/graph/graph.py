from langgraph.graph import StateGraph, START, END
from graph.state import ZenState
from graph.router import route_ticket

from graph.nodes.priority import evaluate_priority
from graph.nodes.retrieve import retrieve_context
from graph.nodes.generate import generate_response
from graph.nodes.ticket_create import create_ticket
from graph.nodes.ticket_update import update_ticket
from graph.nodes.message_store import store_agent_message

graph = StateGraph(ZenState)

graph.add_node("priority", evaluate_priority)
graph.add_node("retrieve", retrieve_context)
graph.add_node("generate", generate_response)
graph.add_node("create_ticket", create_ticket)
graph.add_node("update_ticket", update_ticket)
graph.add_node("store_agent_message", store_agent_message)

graph.add_edge(START, "priority")
graph.add_edge("priority", "retrieve")
graph.add_edge("retrieve", "generate")

graph.add_conditional_edges(
    "generate",
    route_ticket,
    {
        "new_ticket": "create_ticket",
        "existing_ticket": "update_ticket"
    }
)

graph.add_edge("create_ticket", "store_agent_message")
graph.add_edge("update_ticket", "store_agent_message")
graph.add_edge("store_agent_message", END)

ticket_agent = graph.compile()
