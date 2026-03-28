
import streamlit as st
import re
from rag import process_urls, generate_answer

def clean_answer(text):
    """Strip any stray HTML tags the LLM chain may include in its output."""
    return re.sub(r'<[^>]+>', '', text).strip()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Real Estate Research Tool",
    page_icon="🏠",
    layout="wide",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:      #0f1117;
    --surface: #181c27;
    --border:  #252a38;
    --accent:  #c8a96e;
    --accent2: #e8c98e;
    --text:    #e8e4da;
    --muted:   #7a8099;
    --user-bg: #1e2435;
    --bot-bg:  #151922;
    --success: #4caf7d;
    --radius:  14px;
}

html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 16px !important;
}

section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * {
    color: var(--text) !important;
    font-size: 15px !important;
}

#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2rem !important; }

/* ── Title ── */
h1.re-title {
    font-family: 'DM Serif Display', serif !important;
    font-size: 3.2rem !important;
    background: linear-gradient(135deg, #e8c98e 0%, #c8a96e 60%, #a07840 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    letter-spacing: -0.5px;
    margin-bottom: 1.5rem;
    padding: 0;
}

/* ── Sidebar URL inputs ── */
div[data-testid="stTextInput"] label {
    font-size: 1rem !important;
    color: var(--muted) !important;
}
div[data-testid="stTextInput"] input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-size: 0.95rem !important;
    padding: 8px 12px !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(200,169,110,0.15) !important;
}

/* ── Buttons ── */
div[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, var(--accent), #a07840) !important;
    color: #0f1117 !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 1rem !important;
    transition: opacity 0.2s, transform 0.1s !important;
}
div[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Chat bubbles ── */
.chat-wrapper {
    display: flex;
    flex-direction: column;
    gap: 22px;
    padding-bottom: 16px;
}
.msg-row {
    display: flex;
    gap: 14px;
    align-items: flex-start;
    animation: fadeUp 0.3s ease both;
}
.msg-row.user { flex-direction: row-reverse; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

.avatar {
    width: 40px; height: 40px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
    flex-shrink: 0;
}
.avatar.user-av { background: rgba(200,169,110,0.18); border: 1px solid var(--accent); }
.avatar.bot-av  { background: rgba(76,175,125,0.12);  border: 1px solid var(--success); }

.bubble {
    max-width: 75%;
    padding: 16px 22px;
    border-radius: var(--radius);
    font-size: 1.15rem !important;
    line-height: 1.8;
}
.bubble.user {
    background: var(--user-bg);
    border: 1px solid var(--border);
    border-top-right-radius: 4px;
    color: var(--text);
}
.bubble.bot {
    background: var(--bot-bg);
    border: 1px solid var(--border);
    border-top-left-radius: 4px;
    color: var(--text);
}

/* ── Sources ── */
.sources-row {
    margin-left: 54px;
    margin-top: -8px;
    margin-bottom: 4px;
}
.source-label {
    font-size: 0.78rem !important;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}
.source-tag {
    display: inline-block;
    font-size: 0.88rem !important;
    color: var(--accent);
    background: rgba(200,169,110,0.08);
    border: 1px solid rgba(200,169,110,0.2);
    padding: 5px 14px;
    border-radius: 20px;
    text-decoration: none;
    word-break: break-all;
    margin-right: 6px;
    margin-top: 4px;
}
.source-tag:hover { background: rgba(200,169,110,0.18); }

/* ── Chat input ── */
div[data-testid="stChatInput"] textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-size: 1.05rem !important;
    font-family: 'DM Sans', sans-serif !important;
}
div[data-testid="stChatInput"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(200,169,110,0.12) !important;
}

/* ── Status pill ── */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.88rem !important;
    font-weight: 500;
    margin-bottom: 10px;
}
.status-pill.ready {
    background: rgba(76,175,125,0.12);
    border: 1px solid rgba(76,175,125,0.3);
    color: var(--success);
}
.status-pill.idle {
    background: rgba(122,128,153,0.1);
    border: 1px solid var(--border);
    color: var(--muted);
}

.sidebar-label {
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--muted);
    margin-bottom: 6px;
    margin-top: 16px;
}

hr { border-color: var(--border) !important; margin: 1rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "urls_processed" not in st.session_state:
    st.session_state.urls_processed = False
if "processed_urls" not in st.session_state:
    st.session_state.processed_urls = []

# ── Clean any old cached messages that still have stray HTML ──────────────────
st.session_state.chat_history = [
    {**entry, "content": clean_answer(entry["content"])} if entry["role"] == "bot" else entry
    for entry in st.session_state.chat_history
]

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<p style="font-family:\'DM Serif Display\',serif;font-size:1.6rem;'
        'background:linear-gradient(135deg,#e8c98e,#c8a96e);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:0;">'
        '🏠 RE Research</p>',
        unsafe_allow_html=True
    )
    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-label">Data Sources</p>', unsafe_allow_html=True)

    urls = []
    for i in range(1, 4):
        url = st.text_input(f"URL {i}", key=f"url_{i}", placeholder="https://...")
        if url.strip():
            urls.append(url.strip())

    st.markdown('<br>', unsafe_allow_html=True)

    if st.button("⚡ Process URLs"):
        if not urls:
            st.error("Please enter at least one URL.")
        else:
            with st.status("Processing...", expanded=True) as status_box:
                for msg in process_urls(urls):
                    st.write(msg)
                status_box.update(label="✅ Ready to answer questions!", state="complete")
            st.session_state.urls_processed = True
            st.session_state.processed_urls = urls
            st.session_state.chat_history = []
            st.rerun()

    st.markdown('<hr>', unsafe_allow_html=True)

    if st.session_state.urls_processed:
        st.markdown('<div class="status-pill ready">● Sources loaded</div>', unsafe_allow_html=True)
        for u in st.session_state.processed_urls:
            st.markdown(
                f'<p style="font-size:0.82rem;color:#7a8099;word-break:break-all;margin:2px 0;">{u}</p>',
                unsafe_allow_html=True
            )
    else:
        st.markdown('<div class="status-pill idle">○ No sources loaded</div>', unsafe_allow_html=True)

    if st.session_state.chat_history:
        st.markdown('<br>', unsafe_allow_html=True)
        if st.button("🗑 Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

# ── Main panel ─────────────────────────────────────────────────────────────────
st.markdown('<h1 class="re-title">Real Estate Research Tool</h1>', unsafe_allow_html=True)

if not st.session_state.urls_processed:
    st.info("👈 Add one or more article URLs in the sidebar, then click **Process URLs** to begin.", icon="🏗️")

# ── Chat history ───────────────────────────────────────────────────────────────
if st.session_state.chat_history:
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
    for entry in st.session_state.chat_history:
        if entry["role"] == "user":
            st.markdown(f"""
            <div class="msg-row user">
                <div class="avatar user-av">👤</div>
                <div class="bubble user">{entry["content"]}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-row">
                <div class="avatar bot-av">🏠</div>
                <div class="bubble bot">{entry["content"]}</div>
            </div>""", unsafe_allow_html=True)

            if entry.get("sources"):
                src_links = "".join(
                    f'<a class="source-tag" href="{s.strip()}" target="_blank">{s.strip()}</a>'
                    for s in entry["sources"].split(",") if s.strip()
                )
                st.markdown(
                    f'<div class="sources-row"><div class="source-label">Sources</div>{src_links}</div>',
                    unsafe_allow_html=True
                )
    st.markdown('</div>', unsafe_allow_html=True)

# ── Chat input ─────────────────────────────────────────────────────────────────
if st.session_state.urls_processed:
    query = st.chat_input("Ask anything about the loaded articles…")
    if query:
        st.session_state.chat_history.append({"role": "user", "content": query})

        with st.spinner("Thinking…"):
            try:
                answer, sources = generate_answer(query)
                answer = clean_answer(answer)
            except Exception as e:
                answer = f"⚠️ Error: {str(e)}"
                sources = ""

        st.session_state.chat_history.append({
            "role": "bot",
            "content": answer,
            "sources": sources
        })
        st.rerun()