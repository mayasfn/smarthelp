from pydantic import BaseModel, Field
from backend.graph.state import ZenState
from backend.llm.model import llm
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Define the structured format
class AssistantResponse(BaseModel):
    answer: str = Field(description="The helpful response to the user.")
    is_resolved: bool = Field(description="True if the user's issue is resolved.")

def map_role(db_role):
    if db_role == "USER":
        return "human"
    if db_role in ["AGENT_AI", "AGENT_HUMAN"]:
        return "assistant"
    return "human"

def generate_response(state: ZenState) -> dict:
    context = "\n---\n".join(state.get("context", []))
    
    structured_llm = llm.with_structured_output(AssistantResponse)

    system_instructions = """You are 'Zen Agent', a professional technical support assistant.
Your goal is to provide accurate, concise, and helpful answers based ONLY on the provided Context.

RULES:
1. If the Context contains the answer, use it.
2. If the Context is empty or doesn't contain the answer,
Generate a helpful answer based on the user's message and your general knowledge. 
However, if a human intervention is required, please say so, and mention "I will create a ticket for a human agent to assist you."
3. Always maintain a polite, professional tone.
4. If the priority is URGENT, start by acknowledging the urgency.
5. Only mark the issue as resolved if the agent itself could fully address the problem (e.g., by providing information, instructions, or guidance). 
If the ticket requires real-world action by a human (e.g., a physical repair, adding equipment, an HR task, a workplace change), do NOT mark it as resolved even if the user says 'thank you' or expresses satisfaction — the ticket must remain open for the assigned team to act on.
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
    *[ (AIMessage(content=m["content"]) if map_role(m["role"]) == "assistant" 
        else HumanMessage(content=m["content"])) 
       for m in state.get("messages", []) ],
    HumanMessage(content=state['user_message'])
    ]
    
    result = structured_llm.invoke(messages)
    
    return {
        "response": result.answer,
        "is_resolved": result.is_resolved
    }