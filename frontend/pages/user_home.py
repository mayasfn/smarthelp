import streamlit as st
from pathlib import Path
import base64

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def render_home():
    # ---- HERO SECTION ----
    BASE_DIR = Path(__file__).resolve().parent.parent  # frontend/
    css_path = BASE_DIR / "styles.css"
    banner_path = BASE_DIR / "banner.png"
    css = css_path.read_text()
    banner_base64 = img_to_base64(banner_path)
    st.markdown(
           f"""
           <style>
           {css}   
           .hero {{
                background-image:
                   linear-gradient(
                       rgba(0, 0, 0, 0.25),
                       rgba(0, 0, 0, 0.25)
                   ),
                   url("data:image/png;base64,{banner_base64}");   
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;   
                padding: 40px 20px;
                border-radius: 12px;
                color: white;
                text-align: center;
                width: 100vw;
                position: relative;
                left: 50%;
                right: 50%;
                margin-left: -50vw;
                margin-right: -50vw;
                margin-top: 0;

           }}
           </style>
           """,
           unsafe_allow_html=True
       )
       # ---- HERO CONTENT ----
    st.markdown(
        """
        <div class="hero">
            <h1>Support Desk</h1>
            <h2>How can we help you today?</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)


    # ---- SEARCH + CTA ----
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.button("Raise a Problem", use_container_width=True):
            st.session_state.page = "user_chat"
            st.rerun()

    st.markdown("<div style='height:50px'></div>", unsafe_allow_html=True)

    # ---- CARDS ----
    _, c1, c2, _ = st.columns([0.5, 1.5, 1.5, 0.5])


    with c1:
            with st.form("ticket_status_form"):
                st.markdown("### 🔎 Check Ticket Status")
                st.markdown("<p style='font-size:16px;'>Enter your ID to check status.</p>", unsafe_allow_html=True)

                st.markdown('<div class="inline-input">', unsafe_allow_html=True)
                col_id_text, col_id_input = st.columns([1, 2])
                with col_id_text:
                    st.markdown("<p style='margin-top:8px'>Ticket ID:</p>", unsafe_allow_html=True)
                with col_id_input:
                    ticket_id = st.text_input("Ticket ID", label_visibility="collapsed")
                st.markdown('</div>', unsafe_allow_html=True)

                status_submit = st.form_submit_button("View Status")
                if status_submit and ticket_id.strip():
                    st.session_state.page = "ticket_status"
                    #st.session_state.ticket_id = ticket_id.strip()
                    st.rerun()

    with c2:
        with st.form("past_tickets_form"):
            st.markdown("### 📂 View Past Tickets")
            st.markdown("<p style='font-size:16px;'>Access your full history of previous tickets.</p>", unsafe_allow_html=True)
            # Spacer to align with the input field on the left card
            st.markdown("<div style='height:78px'></div>", unsafe_allow_html=True)
            history_submit = st.form_submit_button("Browse History")
            if history_submit:
                st.session_state.page = "past_tickets"
                st.rerun()
            

    # ---- KNOWLEDGE BASE ----
    _, footer_col, _ = st.columns([1, 1.5, 1])
    with footer_col:
        st.markdown(
            """
            <div class="kb">
                <h4>Urgent?</h4>
                <div class="kb-item">
                    <strong>Hotline: 3333</strong><br/>
                    <small>Office hours: Mon-Fri, 9am - 7pm</small>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
