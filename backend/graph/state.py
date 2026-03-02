from typing import TypedDict, Optional, List

class ZenState(TypedDict, total=False):
    ticket_id: Optional[str]
    user_message: str

    priority: str
    context: List[str]
    response: str
    
    messages: List[dict]
    is_resolved: bool
    is_new_ticket: bool
    