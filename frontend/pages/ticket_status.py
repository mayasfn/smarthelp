import streamlit as st

def render_ticket_status():
    st.markdown("""

        <style>
        /* --- PAGE RESET --- */
        section[data-testid="stSidebar"] {display:none;}
        header {visibility:hidden;}         </style>""")
    st.markdown(
        """
        <div class="hero">
            <h1>todo</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
