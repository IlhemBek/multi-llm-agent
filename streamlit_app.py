import streamlit as st
import sys
import os
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.agent import run_agent

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-LLM AI Agent",
    page_icon="🤖",
    layout="centered"
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    .main-title { font-size: 2rem; font-weight: 700; color: #1a1a2e; }
    .subtitle   { color: #666; margin-bottom: 1.5rem; }
    .tool-badge {
        display: inline-block;
        background: #e8f4f8;
        border-radius: 12px;
        padding: 3px 10px;
        font-size: 0.8rem;
        margin: 2px;
        color: #2c7bb6;
    }
    .response-box {
        background: #f8f9fa;
        border-left: 4px solid #2c7bb6;
        padding: 1rem;
        border-radius: 4px;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.markdown('<p class="main-title">🤖 Multi-LLM AI Agent</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Powered by LangChain · Claude API · Groq</p>', unsafe_allow_html=True)

st.markdown("""
**Available tools:**
<span class="tool-badge">🌤 Weather</span>
<span class="tool-badge">🧮 Calculator</span>
<span class="tool-badge">🔍 Web Search</span>
""", unsafe_allow_html=True)

st.divider()

# ── Sidebar settings ─────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    
    provider = st.selectbox(
        "LLM Provider",
        ["claude", "groq"],
        format_func=lambda x: "🟣 Claude (Anthropic)" if x == "claude" else "🟠 Groq (LLaMA 3.3)"
    )
    
    if provider == "claude":
        model = st.selectbox("Model", ["claude-sonnet-4-6", "claude-haiku-4-5-20251001"])
    else:
        model = st.selectbox("Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
    
    st.divider()
    st.markdown("**💡 Example queries:**")
    examples = [
        "What's the weather in Paris?",
        "What is 15% of 8500?",
        "What is LangChain?",
        "Weather in London and convert 20°C to °F",
    ]
    for ex in examples:
        if st.button(ex, use_container_width=True):
            st.session_state["example_query"] = ex

# ── Chat history ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Input ────────────────────────────────────────────────────
default_query = st.session_state.pop("example_query", "")
query = st.chat_input("Ask me anything...", key="chat_input") or default_query

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
    
    with st.chat_message("assistant"):
        with st.spinner(f"Thinking with {provider.capitalize()}..."):
            result = run_agent(query=query, provider=provider, model=model)
        
        if result["success"]:
            response = result["response"]
            st.markdown(response)
            st.caption(f"Powered by **{provider.capitalize()}** · model: `{model}`")
        else:
            error_msg = f"⚠️ Error: {result.get('error', 'Unknown error occurred.')}"
            st.error(error_msg)
            response = error_msg
        
        st.session_state.messages.append({"role": "assistant", "content": response})

# ── Footer ───────────────────────────────────────────────────
st.divider()
st.caption("Built with LangChain · FastAPI · Streamlit | GitHub: [your-username/multi-llm-agent]")
