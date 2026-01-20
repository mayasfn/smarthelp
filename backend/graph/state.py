from typing import TypedDict, Optional, List

class ZendeskState(TypedDict, total=False):
    ticket_id: Optional[str]
    user_message: str

    priority: str
    context: List[str]
    response: str

    is_new_ticket: bool
    