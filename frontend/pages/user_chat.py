import streamlit as st
from backend.agent_mock import run_agent_mock

def render_user_chat():
    # --- STATE INIT ---
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "ticket_id" not in st.session_state:
        st.session_state.ticket_id = None

    # --- TOP NAVIGATION BAR ---
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
    
    with nav_col1:
        if st.button("🏠 Home"):
            st.session_state.page = "home"
            st.rerun()

    with nav_col2:
        st.markdown(
            f"<h3 style='text-align: center; margin-top: -10px;'>{'Ticket #' + str(st.session_state.ticket_id) if st.session_state.ticket_id else 'New Support Request'}</h3>", 
            unsafe_allow_html=True
        )

    with nav_col3:
        if st.session_state.ticket_id:
            if st.button("Close Ticket", type="primary"):
                # Reset ticket state and go home
                st.toast(f"Ticket #{st.session_state.ticket_id} has been closed!")
                st.session_state.ticket_id = None
                st.session_state.messages = []
                st.session_state.page = "home"
                st.rerun()

    st.divider()

    # --- MESSAGE RENDERER ---
    chat_box = st.container()

    with chat_box:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
                if msg.get("ticket_id"):
                    p_color = {"HIGH": "#ef4444", "MEDIUM": "#f97316", "LOW": "#22c55e"}.get(msg.get("priority", "LOW"))
                    st.markdown(
                        f"""<div style="font-size: 0.8rem; margin-top: 5px; opacity: 0.8;">
                            <span style="background: #eee; padding: 2px 6px; border-radius: 4px;">ID: #{msg['ticket_id']}</span> 
                            <span style="color: {p_color}; font-weight: bold;">{msg.get('priority')} Priority</span>
                        </div>""", 
                        unsafe_allow_html=True
                    )

    # --- CHAT INPUT ---
    if prompt := st.chat_input("Describe your issue..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with chat_box:
            with st.chat_message("user"):
                st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                response = run_agent_mock(prompt, st.session_state.ticket_id)
                
                st.session_state.ticket_id = response.get("ticket_id")
                new_msg = {
                    "role": "assistant",
                    "content": response["response"],
                    "ticket_id": response.get("ticket_id"),
                    "priority": response.get("priority", "LOW"),
                }
                st.session_state.messages.append(new_msg)
                st.rerun()