from pydantic import BaseModel, Field
from backend.graph.state import ZenState
from backend.llm.model import llm
from langchain_core.messages import HumanMessage, SystemMessage

# Define the structured format
class AssistantResponse(BaseModel):
    answer: str = Field(description="The helpful response to the user.")
    is_resolved: bool = Field(description="True if the user's issue is resolved.")

def generate_response(state: ZenState) -> dict:
    context = "\n---\n".join(state.get("context", []))
    
    structured_llm = llm.with_structured_output(AssistantResponse)

    system_instructions = """You are 'Zen Agent', a professional technical support assistant.
Your goal is to provide accurate, concise, and helpful answers based ONLY on the provided Context.

RULES:
1. If the Context contains the answer, use it.
2. If the Context is empty or doesn't contain the answer, say: "I'm sorry, I couldn't find a specific internal guide for this issue. Let me create a ticket for a human agent to assist you."
3. Always maintain a polite, professional tone.
4. If the priority is URGENT, start by acknowledging the urgency.
5. If the user's latest input indicates their problem is fully resolved 
    or if they are expressing final satisfaction (e.g., 'thank you', 'that worked') then include in your response that you are closing the ticket and mark the issue as resolved.
6. Always answer in the same language as the user's message.
"""
    user_string = f"""
Priority: {state.get('priority', 'LOW')}
Question: {state['user_message']}
Context: {context}

Helpful Answer:
"""

    messages = [
        SystemMessage(content=system_instructions),
        *state.get("messages", []), # Include history for context
        HumanMessage(content=user_string)
    ]
    
    # 2. Single LLM call for BOTH answer and resolution
    result = structured_llm.invoke(messages)
    
    # Return both the response text and a resolution flag to the graph state
    return {
        "response": result.answer,
        "is_resolved": result.is_resolved
    }