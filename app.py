import streamlit as st

st.set_page_config(
    page_title="Bug Ticket Agent",
    page_icon="🐛",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    [data-testid="stSidebar"] { background: #1a1a2e; }
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    .stTextArea textarea {
        font-family: monospace !important;
        font-size: 13px !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.markdown("## 🐛 Bug Ticket Agent")
st.sidebar.markdown("---")

pages = {
    "🔍 Bug Analyzer": "chat",
    "🎫 Ticket Dashboard": "tickets",
}

if "page" not in st.session_state:
    st.session_state.page = "chat"

for label, key in pages.items():
    if st.sidebar.button(
        label,
        use_container_width=True,
        type="primary" if st.session_state.page == key else "secondary"
    ):
        st.session_state.page = key
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### How it works")
st.sidebar.markdown("""
1. 📋 Paste your code
2. 🤖 AI detects bugs
3. 🔍 FAISS checks duplicates
4. 💾 SQLite saves ticket
5. 📤 GitHub issue created
""")
st.sidebar.markdown("---")
st.sidebar.caption("Built with HuggingFace + FAISS + SQLite + GitHub API")

# Route pages
page = st.session_state.page

if page == "chat":
    from pages import chat
    chat.render()
elif page == "tickets":
    from pages import tickets
    tickets.render()