import streamlit as st
from backend.db.zen_repo import ZenRepository

def render_admin_dashboard():
    repo = ZenRepository()
    
    # Custom CSS for UI Toggles
    st.markdown("""
        <style>
        div[data-testid="stSegmentedControl"] button[aria-checked="true"] {
            background-color: #2e7d32 !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🎫 Administrator Dashboard")

    # --- FILTERS & SORTING ---
    top_col1, top_col2, top_col3 = st.columns([2, 2, 1])
    with top_col1:
        filter_status = st.segmented_control(
            "Filter by Status",
            options=["All", "OPEN", "CLOSED"],
            default="All"
        )

    with top_col2:
        sort_col = st.selectbox(
            "Sort By", 
            options=["Last updated", "Creation Date", "Priority", "Status", "Subject", "Type", "Queue"]
        )

    with top_col3:
        sort_order = st.radio("Order", ["DESC", "ASC"], horizontal=True)

    tickets = repo.get_all_tickets()

    # Collect distinct values for Type and Queue filters
    all_types = sorted({t['TYPE'] for t in tickets if t.get('TYPE')})
    all_queues = sorted({t['QUEUE'] for t in tickets if t.get('QUEUE')})

    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        filter_types = st.multiselect(
            "Filter by Type",
            options=all_types,
            placeholder="All types"
        )
    with filter_col2:
        filter_queues = st.multiselect(
            "Filter by Queue",
            options=all_queues,
            placeholder="All queues"
        )

    if filter_status != "All":
        tickets = [t for t in tickets if t['STATUS'] == filter_status]
    if filter_types:
        tickets = [t for t in tickets if t.get('TYPE') in filter_types]
    if filter_queues:
        tickets = [t for t in tickets if t.get('QUEUE') in filter_queues]

    # Sorting Logic
    priority_map = {"URGENT": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    rev = True if sort_order == "DESC" else False
    if sort_col == "Priority":
        tickets.sort(key=lambda x: priority_map.get(x['PRIORITY'], 4), reverse=rev)
    elif sort_col == "Last updated":
        tickets.sort(key=lambda x: x.get('UPDATED_AT') or x['CREATED_AT'], reverse=rev)
    elif sort_col == "Creation Date":
        tickets.sort(key=lambda x: x['CREATED_AT'], reverse=rev)
    else:
        tickets.sort(key=lambda x: str(x.get(sort_col.upper(), "")), reverse=rev)

    st.divider()

    # --- CARD GRID ---
    if not tickets:
        st.info("No tickets found.")
    else:
        cols = st.columns(3)
        for idx, t in enumerate(tickets):
            with cols[idx % 3]:
                p_color = {"URGENT": "#ef4444", "HIGH": "#f97316", "MEDIUM": "#3b82f6", "LOW": "#22c55e"}.get(t['PRIORITY'], "#6c757d")
                status_bg = "#d4edda" if t['STATUS'] == 'OPEN' else "#f8d7da"
                status_text = "#155724" if t['STATUS'] == 'OPEN' else "#721c24"
                
                updated_val = t.get('UPDATED_AT') or t['CREATED_AT']

                raw_subject = str(t.get('SUBJECT', '')).strip()
                display_subject = raw_subject if len(raw_subject) > 10 else "[No Subject]"
                
                with st.container(border=True):
                    st.markdown(f"""
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <code style='color: #888;'>#{t['TICKET_ID'][:8]}</code>
                            <span style='background-color: {status_bg}; color: {status_text}; 
                                  padding: 2px 10px; border-radius: 20px; font-size: 0.7rem; 
                                  font-weight: bold;'>{t['STATUS']}</span>
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                        <div style='height: 60px; overflow: hidden; margin-top: 10px;'>
                            <h3 style='margin: 0; font-size: 1.15rem;'>{display_subject[:50]}...</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"**Priority:** <span style='color:{p_color};'>{t['PRIORITY']}</span>", unsafe_allow_html=True)

                    tag_type = t.get('TYPE') or '—'
                    tag_queue = t.get('QUEUE') or '—'
                    st.markdown(
                        f"<div style='margin-top:4px; font-size:0.8rem;'>"
                        f"<span style='background:#e0e7ff; color:#3730a3; padding:2px 8px; "
                        f"border-radius:12px; margin-right:6px;'>🏷 {tag_type}</span>"
                        f"<span style='background:#fef3c7; color:#92400e; padding:2px 8px; "
                        f"border-radius:12px;'>📋 {tag_queue}</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )

                    st.markdown(f"""
                        <p style='font-style: italic; font-size: 0.8rem; color: #666; margin-bottom: 0;'>
                            Last updated: {updated_val.strftime('%Y-%m-%d %H:%M')}
                        </p>
                        <p style='font-style: italic; font-size: 0.8rem; color: #666; margin-top: 0;'>
                            Creation: {t['CREATED_AT'].strftime('%Y-%m-%d %H:%M')}
                        </p>
                    """, unsafe_allow_html=True)

                    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button("💬 Open", key=f"open_{t['TICKET_ID']}", width='stretch'):
                            st.session_state.ticket_id = t['TICKET_ID']
                            st.session_state.page = "user_chat"
                            st.rerun()
                    with btn_col2:
                        if t['STATUS'] == 'OPEN':
                            if st.button("🛑 Close", key=f"close_{t['TICKET_ID']}", type="primary", width='stretch'):
                                repo.close_ticket(t['TICKET_ID'])
                                st.rerun()
                        else:
                            st.button("Closed", key=f"dis_{t['TICKET_ID']}", disabled=True, width='stretch')
