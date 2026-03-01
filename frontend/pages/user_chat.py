import streamlit as st
from backend.agent import run_agent

def render_user_chat():
    # --- STATE INIT ---
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "ticket_id" not in st.session_state:
        st.session_state.ticket_id = None
    if "error_message" not in st.session_state:
        st.session_state.error_message = None

    # --- TOP NAVIGATION BAR ---
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
    
    with nav_col1:
        if st.button("🏠 Home"):
            st.session_state.page = "home"
            st.session_state.error_message = None # Clear errors on nav
            st.rerun()

    with nav_col2:
        if st.session_state.ticket_id:
            priority = st.session_state.get("priority", "LOW")
            p_color = {"URGENT": "#ef4444", "HIGH": "#f97316", "MEDIUM": "#3b82f6", "LOW": "#22c55e"}.get(priority)
            
            st.markdown(
                f"""
                <div style='text-align: center; margin-top: -10px;'>
                    <h3 style='margin-bottom: 0;'>Ticket #{st.session_state.ticket_id}</h3>
                    <span style='background-color: {p_color}; color: white; padding: 2px 10px; 
                                 border-radius: 12px; font-size: 0.8rem; font-weight: bold; 
                                 text-transform: uppercase;'>
                        {priority}
                    </span>
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<h3 style='text-align: center; margin-top: -10px;'>New Support Request</h3>", 
                unsafe_allow_html=True
            )

    with nav_col3:
        if st.session_state.ticket_id:
            if st.button("Close Ticket", type="primary"):
                st.toast(f"Ticket #{st.session_state.ticket_id} has been closed!")
                st.session_state.ticket_id = None
                st.session_state.messages = []
                st.session_state.error_message = None
                st.session_state.page = "home"
                st.rerun()

    st.divider()

    # --- ERROR DISPLAY ---
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
        if st.button("Clear Error"):
            st.session_state.error_message = None
            st.rerun()

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
        st.session_state.error_message = None
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with chat_box:
            with st.chat_message("user"):
                st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response_state = run_agent(prompt, st.session_state.ticket_id)
                    
                    st.session_state.ticket_id = response_state.get("ticket_id")
                    st.session_state.priority = response_state.get("priority", "LOW")
                    
                    new_msg = {
                        "role": "assistant",
                        "content": response_state["response"],
                        "ticket_id": response_state.get("ticket_id"),
                        "priority": response_state.get("priority", "LOW"),
                    }
                    st.session_state.messages.append(new_msg)
                    st.rerun()

                except Exception as e:
                    print(f"CRITICAL AGENT ERROR: {e}")
                    st.session_state.error_message = e
                    st.error(st.session_state.error_message)