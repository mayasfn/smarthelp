import os
import streamlit as st

from backend.db.zen_repo import ZenRepository

@st.cache_resource
def get_repo():
    return ZenRepository()

def render_past_tickets():
    st.markdown("## 📂 Your Ticket History")
    
    try:
        repo = get_repo()
        tickets = repo.get_user_tickets()  
        if not tickets:
            st.info("You haven't created any tickets yet.")
            if st.button("Create your first ticket"):
                st.session_state.page = "user_chat"
                st.rerun()
        else:
            st.dataframe(
                tickets,
                column_config={
                    "TICKET_ID": "ID",
                    "SUBJECT": "Issue Description",
                    "PRIORITY": st.column_config.TextColumn("Priority"),
                    "STATUS": "Status",
                    "TYPE": "Type",
                    "QUEUE": "Queue",
                    "CREATED_AT": st.column_config.DatetimeColumn("Date Created")
                },
                hide_index=True,
                width='stretch'
            )
            
            if st.button("⬅️ Back to Home"):
                st.session_state.page = "home"
                st.rerun()

    except Exception as e:
        st.error(f"Could not load tickets: {e}")
