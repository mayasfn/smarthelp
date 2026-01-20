from graph.state import ZenState
from db.snowflake import get_session
from snowflake.core import Root
import os

def retrieve_context(state: ZenState) -> dict:
    session = get_session()
    root = Root(session)

    service = (
        root
        .databases[os.getenv("DATABASE")]
        .schemas[os.getenv("SCHEMA")]
        .cortex_search_services[os.getenv("CORTEX_SEARCH_SERVICE")]
    )

    resp = service.search(
        query=state["user_message"],
        columns=["body_answer"],
        limit=5
    )

    context = [r["body_answer"] for r in resp.results] if resp.results else []
    return {"context": context}
