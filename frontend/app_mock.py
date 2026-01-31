import streamlit as st
from streamlit_option_menu import option_menu
import sys
from pathlib import Path
import time

# --- BACKEND MOCK ---
try:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from backend.agent_mock import run_agent_mock as run_agent
except ImportError:
    def run_agent(user_message, ticket_id):
        time.sleep(1)
        return {
            "response": f"Received. Processing your request: '{user_message}'.",
            "ticket_id": ticket_id if ticket_id else f"TKT-{int(time.time())}",
            "priority": "HIGH"
        }

# --- CONFIG ---
st.set_page_config(
    page_title="Assistant Support",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS FINAL ---
st.markdown("""
<style>
    /* 1. FOND & TEXTE */
    .stApp {
        background-color: #ffffff;
        font-family: 'Segoe UI', Helvetica, sans-serif;
    }

    /* 2. FIX SIDEBAR (HEADER TRANSPARENT MAIS VISIBLE) */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        z-index: 1;
    }
    div[data-testid="stDecoration"] {
        display: none;
    }
    footer { display: none; }

    /* 3. MAIN CONTAINER */
    div[data-testid="stMainBlockContainer"] {
        max-width: 850px !important;
        margin: 0 auto !important;
        padding-top: 4rem !important;
        padding-bottom: 10rem !important;
    }

    /* 4. INPUT BAR FIX */
    div[data-testid="stBottom"] {
        background-color: transparent !important;
        border: none !important;
        padding-bottom: 20px;
    }

    div[data-testid="stChatInput"] {
        max-width: 850px !important;
        width: 100% !important;
        margin: 0 auto !important;
        position: relative;
    }

    /* BOUTON ENVOYER (Violet clair) */
    div[data-testid="stChatInput"] button {
        display: none !important;
        background: transparent !important;
        color: #a78bfa !important;
        border: none !important;
        width: 40px !important;
        height: 40px !important;
        position: absolute !important;
        right: 15px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        z-index: 5 !important;
    }
    
    div[data-testid="stChatInput"] button:hover {
        background-color: #f3e8ff !important;
        border-radius: 50% !important;
    }

    /* Style de la textarea (input) */
    .stChatInput textarea {
        background-color: #ffffff !important;
        border: 1px solid #f3e8ff !important;
        border-radius: 30px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
        min-height: 60px !important;
        padding: 18px 60px 18px 30px !important; 
        line-height: 1.5 !important;
        font-size: 16px !important;
        overflow: hidden !important;
        color: #1f1f1f !important;
        caret-color: #a78bfa !important;
    }

    .stChatInput textarea::placeholder {
        color: #9ca3af !important;
        opacity: 1;
    }

    /* FOCUS INPUT: Suppression du halo lumineux (box-shadow) et du contour */
    .stChatInput textarea:focus, .stChatInput textarea:focus-visible {
        border-color: #f3e8ff !important; /* On garde la bordure très pâle ou mettez transparent si voulu */
        box-shadow: none !important; /* PLUS AUCUN HALO */
        background-color: #ffffff !important;
        outline: none !important;
    }
            
    /* 5. DESIGN DES BULLES */
    .chat-row { display: flex; width: 100%; margin-bottom: 20px; }
    .row-user { justify-content: flex-end; }
    .row-bot { justify-content: flex-start; }

    /* BULLE UTILISATEUR: Violet Clair */
    .msg-user {
        background: #90B7CF;
        color: white;
        padding: 12px 18px;
        border-radius: 20px 20px 4px 20px;
        max-width: 80%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        font-size: 15px;
    }

    .msg-bot {
        background-color: #f8fafc;
        color: #1f1f1f;
        padding: 12px 18px;
        border-radius: 20px 20px 20px 4px;
        max-width: 80%;
        border: 1px solid #e2e8f0;
        font-size: 15px;
    }

    .bot-avatar { font-size: 28px; margin-right: 12px; display: flex; align-items: flex-end;}

    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #f8f9fa; border-right: 1px solid #e9ecef; }
    
    /* BOUTON NOUVELLE CONVERSATION (VIOLET CLAIR - FIX FORCE) */
    section[data-testid="stSidebar"] button {
        background-color: #5FACD3 !important; /* Fallback */
        background: #5FACD3 !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(95, 172, 211, 0.2) !important;
    }
    
    section[data-testid="stSidebar"] button:hover {
        opacity: 0.9 !important;
        box-shadow: 0 6px 12px rgba(95, 172, 211, 0.4) !important;
        transform: translateY(-1px) !important;
        color: white !important;
    }
    
    section[data-testid="stSidebar"] button p {
        color: white !important;
    }

    /* Tags */
    .meta-tags { font-size: 11px; margin-top: 6px; display: flex; gap: 8px; opacity: 0.7; }
    .tag-id { font-family: monospace; background: rgba(0,0,0,0.05); padding: 2px 6px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# --- STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "ticket_id" not in st.session_state:
    st.session_state.ticket_id = None

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🛠️ Menu")
    selected = option_menu(
        menu_title=None,
        options=["Assistant", "Analytics", "Settings"],
        icons=["chat-text-fill", "graph-up-arrow", "gear"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px"},
            "nav-link-selected": {"background-color": "#5FACD3"},
        }
    )
    st.divider()
    
    # NEW CONVERSATION BUTTON
    if st.button("➕ New Conversation", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.session_state.ticket_id = None
        st.rerun()

# --- APP ---
if selected == "Assistant":

    if not st.session_state.messages:
        st.markdown("""
            <div style="text-align: center; margin-top: 60px; margin-bottom: 40px;">
                <h2 style="color: #333;">Hello 👋</h2>
                <p style="color: #666;">I'm your daily assistant.</p>
            </div>
        """, unsafe_allow_html=True)

    def render_msg(role, content, ticket=None, priority=None):
        if role == "user":
            return f"""<div class="chat-row row-user"><div class="msg-user">{content}</div></div>"""
        else:
            meta = ""
            if ticket:
                color = "#f97316" if priority == "MEDIUM" else ("#ef4444" if priority == "HIGH" else "#22c55e")
                meta = f"""<div class="meta-tags"><span class="tag-id">#{ticket}</span><span style="color:{color};font-weight:600">{priority}</span></div>"""
            return f"""<div class="chat-row row-bot"><div class="bot-avatar">🤖</div><div class="msg-bot">{content}{meta}</div></div>"""

    chat_container = st.container()

    with chat_container:
        for msg in st.session_state.messages:
            st.markdown(render_msg(msg["role"], msg["content"], msg.get("ticket_id"), msg.get("priority")), unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("Describe your issue here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            st.markdown(render_msg("user", prompt), unsafe_allow_html=True)

        with chat_container:
            with st.empty():
                st.markdown(render_msg("bot", "<i>Thinking...</i>"), unsafe_allow_html=True)
                response = run_agent(prompt, st.session_state.ticket_id)

        st.session_state.ticket_id = response.get("ticket_id")
        st.session_state.messages.append({
            "role": "agent", "content": response["response"],
            "ticket_id": st.session_state.ticket_id, "priority": response.get("priority", "LOW")
        })
        st.rerun()

elif selected == "Analytics":
    st.title("📊 Analytics")
    st.info("Content centered.")

elif selected == "Settings":
    st.title("⚙️ Settings")
    st.info("Settings panel.")