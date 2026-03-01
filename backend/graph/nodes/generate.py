from backend.graph.state import ZenState
from backend.llm.model import llm
from langchain_core.messages import HumanMessage, SystemMessage

def generate_response(state: ZenState) -> dict:
    context = "\n---\n".join(state.get("context", []))

    system_instructions = """You are 'Zen Agent', a professional technical support assistant.
Your goal is to provide accurate, concise, and helpful answers based ONLY on the provided Context.

RULES:
1. If the Context contains the answer, use it.
2. If the Context is empty or doesn't contain the answer, say: "I'm sorry, I couldn't find a specific internal guide for this issue. Let me create a ticket for a human agent to assist you."
3. Always maintain a polite, professional tone.
4. If the priority is URGENT, start by acknowledging the urgency.
"""
    user_string = f"""
Priority: {state.get('priority', 'LOW')}
Question: {state['user_message']}
Context: {context}

Helpful Answer:
"""

    messages = [
        SystemMessage(content=system_instructions),
        HumanMessage(content=user_string)
    ]
    response = llm.invoke(messages).content.strip()
    
    return {"response": response}