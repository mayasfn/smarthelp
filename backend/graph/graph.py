from langgraph.graph import StateGraph, START, END
from backend.graph.state import ZenState
from backend.graph.router import route_ticket

from backend.graph.nodes.load_history import load_ticket_history
from backend.graph.nodes.evaluate import evaluate_ticket
from backend.graph.nodes.retrieve import retrieve_context
from backend.graph.nodes.generate import generate_response
from backend.graph.nodes.ticket_create import create_ticket
from backend.graph.nodes.ticket_update import update_ticket
from backend.graph.nodes.message_store import store_agent_message
from backend.graph.nodes.status_monitor import check_for_resolution

graph = StateGraph(ZenState)

graph.add_node("load_history", load_ticket_history)
graph.add_node("retrieve", retrieve_context)
graph.add_node("evaluate", evaluate_ticket)
graph.add_node("create_ticket", create_ticket)
graph.add_node("update_ticket", update_ticket)
graph.add_node("generate", generate_response)
graph.add_node("store_agent_message", store_agent_message)
graph.add_node("check_for_resolution", check_for_resolution)

graph.add_edge(START, "load_history")
graph.add_edge("load_history", "retrieve")

graph.add_conditional_edges(
    "retrieve",
    route_ticket,
    {
        "new_ticket": "evaluate_ticket",
        "existing_ticket": "update_ticket"
    }
)

graph.add_edge("evaluate", "create_ticket")
graph.add_edge("create_ticket", "generate")
graph.add_edge("update_ticket", "generate")
graph.add_edge("generate", "store_agent_message")
graph.add_edge("store_agent_message", "check_for_resolution")
graph.add_edge("check_for_resolution", END)

ticket_agent = graph.compile()
