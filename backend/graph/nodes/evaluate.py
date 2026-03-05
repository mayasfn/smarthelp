from backend.graph.state import ZenState
from backend.llm.model import llm
from langchain_core.messages import HumanMessage


priority_levels = [
    "HIGH", 
    "MEDIUM", 
    "LOW",
]

types = [
    "Request",
    "Problem",
    "Change",
    "Incident",
]

queues = [
    "Returns and Exchanges",
    "Service Outages and Maintenance",
    "Technical Support",
    "General Inquiry",
    "IT Support",
    "Customer Service",
    "Sales and Pre-Sales",
    "Product Support",
    "Billing and Payments",
    "Human Resources",
]

def parse_response(raw, priority_levels, types, queues):
    subject, priority, type, queue = [part.strip() for part in raw.split(";")]
    if priority.upper() not in priority_levels:
        print(f"Invalid priority level: {priority}. Defaulting to LOW.")
        priority = "LOW"
    if type not in types:
        print(f"Invalid type: {type}. Defaulting to Request.")
        type = "Request"
    if queue not in queues:
        print(f"Invalid queue: {queue}. Defaulting to General Inquiry.")
        queue = "General Inquiry"
    return subject, priority, type, queue


def evaluate_ticket(state: ZenState) -> dict:
    context = "\n---\n".join(state.get("context", []))    

    msg = HumanMessage(
        content=(
            "Classify support ticket subject, priority, type and queue based on the user's message and relevant context from past tickets.\n"
            "Subject: A brief summary of the user's issue, ideally in 5 words or less.\n"
            f"Priority levels: {priority_levels}\n"
            f"Types: {types}\n"
            f"Queues: {queues}\n"
            f"User message: {state['user_message']}\n"
            f"Relevant past tickets: {context if context else 'None'}\n"
            f"Conversation history: {state.get('messages', [])}\n"
            "Please analyze the user's message and the context to determine the appropriate labels for this supprot ticket."
            "Return only the labels in your response, without any additional text or explanation. Format your response as: <subject>; <priority_level>; <type>; <queue>."
        )
    )

    raw = llm.invoke([msg]).content

    subject, priority, type, queue = parse_response(raw, priority_levels, types, queues)

    return {
        "subject": subject,
        "priority": priority,
        "type": type,
        "queue": queue,
    }
