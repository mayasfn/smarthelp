from pydantic import BaseModel, Field
from backend.llm.model import llm  
from backend.db.zen_repo import ZenRepository

class ResolutionSchema(BaseModel):
    """Binary score for ticket resolution."""
    is_resolved: bool = Field(description="True if the user is satisfied and the issue is resolved.")

def check_for_resolution(state):
    ticket_id = state.get("ticket_id")
    if not ticket_id:
        return state
    structured_llm = llm.with_structured_output(ResolutionSchema)

    system_prompt = """Analyze the conversation history. 
    Determine if the user's latest input indicates their problem is fully resolved 
    or if they are expressing final satisfaction (e.g., 'thank you', 'that worked')."""
    
    messages = [{"role": "system", "content": system_prompt}] + state.get("messages", [])
    
    try:
        result = structured_llm.invoke(messages)

        if result.is_resolved:
            repo = ZenRepository()
            repo.session.sql(
                "UPDATE ZEN_TICKETS SET STATUS = 'CLOSED' WHERE TICKET_ID = ?",
                params=[ticket_id]
            ).collect()
            
            state["status"] = "CLOSED"
    except Exception as e:
        print(f"Error checking resolution: {e}")

    return state