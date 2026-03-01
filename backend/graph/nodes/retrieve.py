from ..state import ZenState
from ...db.snowflake import get_session
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
        columns=["body_answer"],
        limit=5
    )

    context = [r["body_answer"] for r in resp.results] if resp.results else []
    return {"context": context}
