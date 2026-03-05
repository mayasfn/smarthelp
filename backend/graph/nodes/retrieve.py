from backend.graph.state import ZenState
from backend.db.snowflake_utils import get_session

from snowflake.core import Root
import os

def retrieve_context(state: ZenState) -> dict:
    session = get_session()
    root = Root(session)

    service = (
        root
        .databases[os.getenv("SNOWFLAKE_DATABASE")]
        .schemas[os.getenv("SNOWFLAKE_SCHEMA")]
        .cortex_search_services[os.getenv("SNOWFLAKE_CORTEX_SEARCH_SERVICE")]
    )

    resp = service.search(
        query=state["user_message"],
        columns=["priority", "subject", "type", "queue", "body_answer"],
        limit=5
    )

    context = []
    if resp.results:
        for result in resp.results:
            priority = result.get("priority", "UNKNOWN")
            subject = result.get("subject", "")
            ticket_type = result.get("type", "")
            answer = result.get("body_answer", "")

            context.append(
                f"Priority={priority}; Subject={subject}; Type={ticket_type}; Resolution={answer}"
            )

    return {"context": context}
