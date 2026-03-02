import streamlit as st
from backend.db.zen_repo import ZenRepository

def render_admin_dashboard():
    repo = ZenRepository()
    st.title("🎫 Admin Ticket Dashboard")

    # --- TOP CONTROLS ---
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Filter tabs
        filter_tab = st.segmented_control(
            "Filter Status", 
            options=["All", "OPEN", "CLOSED"], 
            default="All"
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sort By", 
            options=["Created At", "Priority", "Status", "Subject"]
        )

    # --- DATA FETCHING ---
    tickets = repo.get_all_tickets() #
    
    # Filtering
    if filter_tab != "All":
        tickets = [t for t in tickets if t['STATUS'] == filter_tab]

    # Sorting Logic
    priority_map = {"URGENT": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    if sort_by == "Priority":
        tickets.sort(key=lambda x: priority_map.get(x['PRIORITY'], 4))
    elif sort_by == "Status":
        tickets.sort(key=lambda x: x['STATUS'])
    elif sort_by == "Subject":
        tickets.sort(key=lambda x: x['SUBJECT'])
    else: # Created At
        tickets.sort(key=lambda x: x['CREATED_AT'], reverse=True)

    # --- CARD GRID ---
    if not tickets:
        st.info("No tickets found matching these criteria.")
    else:
        cols = st.columns(3)
        for idx, ticket in enumerate(tickets):
            with cols[idx % 3]:
                p_color = {
                    "URGENT": "#ef4444", 
                    "HIGH": "#f97316", 
                    "MEDIUM": "#3b82f6", 
                    "LOW": "#22c55e"
                }.get(ticket['PRIORITY'], "#6c757d")
                
                status_color = "#28a745" if ticket['STATUS'] == "OPEN" else "#6c757d"

                st.markdown(
                    f"""
                    <div style="
                        border: 1px solid #ddd; 
                        border-radius: 10px; 
                        padding: 15px; 
                        margin-bottom: 20px; 
                        background-color: #f9f9f9;
                        min-height: 200px;
                    ">
                        <div style="display: flex; justify-content: space-between;">
                            <span style="font-size: 0.8rem; color: #666;">ID: {ticket['TICKET_ID'][:8]}</span>
                            <span style="background: {status_color}; color: white; padding: 2px 8px; border-radius: 5px; font-size: 0.7rem;">{ticket['STATUS']}</span>
                        </div>
                        <h4 style="margin: 10px 0;">{ticket['SUBJECT'][:60]}{'...' if len(ticket['SUBJECT']) > 60 else ''}</h4>
                        <div style="margin-top: 10px;">
                            <span style="color: {p_color}; font-weight: bold; font-size: 0.8rem;">● {ticket['PRIORITY']} Priority</span>
                        </div>
                        <div style="font-size: 0.75rem; color: #888; margin-top: 5px;">
                            Last Activity: {ticket['CREATED_AT'].strftime('%Y-%m-%d %H:%M')}
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Action Buttons
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("Open Chat", key=f"chat_{ticket['TICKET_ID']}", use_container_width=True):
                        st.session_state.ticket_id = ticket['TICKET_ID']
                        st.session_state.page = "user_chat"
                        st.rerun()
                with btn_col2:
                    if ticket['STATUS'] == "OPEN":
                        if st.button("Close", key=f"close_{ticket['TICKET_ID']}", type="primary", use_container_width=True):
                            repo.session.sql(
                                "UPDATE ZEN_TICKETS SET STATUS = 'CLOSED' WHERE TICKET_ID = ?", 
                                params=[ticket['TICKET_ID']]
                            ).collect()
                            st.rerun()