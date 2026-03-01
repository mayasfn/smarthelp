import streamlit as st
from backend.db.zen_repo import ZenRepository

def render_past_tickets():
    st.markdown("## 📂 Your Ticket History")
    
    try:
        repo = ZenRepository()
        tickets = repo.get_all_tickets() 
        
        if not tickets:
            st.info("You haven't created any tickets yet.")
            if st.button("Create your first ticket"):
                st.session_state.page = "user_chat"
                st.rerun()
        else:
            # We use a dataframe for a nice, interactive table
            st.dataframe(
                tickets,
                column_config={
                    "TICKET_ID": "ID",
                    "SUBJECT": "Issue Description",
                    "PRIORITY": st.column_config.TextColumn("Priority"),
                    "STATUS": "Status",
                    "CREATED_AT": st.column_config.DatetimeColumn("Date Created")
                },
                hide_index=True,
                use_container_width=True
            )
            
            if st.button("⬅️ Back to Home"):
                st.session_state.page = "home"
                st.rerun()

    except Exception as e:
        st.error(f"Could not load tickets: {e}")