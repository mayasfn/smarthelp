from ..state import ZenState
from ...llm.model import llm
from langchain_core.messages import HumanMessage

def generate_response(state: ZenState) -> dict:
    context = "\n---\n".join(state.get("context", []))

    msg = HumanMessage(content=f"""
Priority: {state['priority']}
Question: {state['user_message']}
Context: {context}

Write a helpful support answer.
""")

    response = llm.invoke([msg]).content.strip()
    return {"response": response}
