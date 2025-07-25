# streamlit_app.py
import os
import asyncio
import atexit
from typing import List, Dict, Any

import streamlit as st

from sidekick import Sidekick  # your existing class


# -----------------------------#
# ------- Page Settings -------#
# -----------------------------#
st.set_page_config(
    page_title="Visexa Pilot",
    page_icon="🧑‍💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------#
# ------- Small Helpers -------#
# -----------------------------#
def run_async(coro):
    """Run async code safely inside Streamlit."""
    return asyncio.run(coro)

def init_session_state():
    ss = st.session_state
    ss.setdefault("sidekick", None)
    ss.setdefault("history", [])
    ss.setdefault("initialized", False)
    ss.setdefault("success_criteria", "The answer should be clear and accurate")
    ss.setdefault("disable_tracing", False)

def setup_sidekick():
    """Create & cache a Sidekick instance once per session."""
    if st.session_state.sidekick is None:
        with st.spinner("Booting your Visexa Pilot"):
            # Optionally disable tracing (LangSmith) for this session
            if st.session_state.disable_tracing:
                os.environ["LANGCHAIN_TRACING_V2"] = "false"

            # Optional: force Playwright headless on Streamlit Cloud
            os.environ.setdefault("PLAYWRIGHT_HEADLESS", "true")

            sk = Sidekick()
            run_async(sk.setup())
            st.session_state.sidekick = sk
            st.session_state.initialized = True

def reset_everything():
    if st.session_state.sidekick:
        try:
            st.session_state.sidekick.cleanup()
        except Exception:
            pass
    st.session_state.sidekick = None
    st.session_state.history = []
    st.session_state.initialized = False
    st.rerun()

def on_app_exit():
    # best effort cleanup (useful locally)
    if "sidekick" in st.session_state and st.session_state.sidekick:
        try:
            st.session_state.sidekick.cleanup()
        except Exception:
            pass

atexit.register(on_app_exit)

# --------------------------------#
# ------- Custom CSS Polish -------#
# --------------------------------#
CUSTOM_CSS = """
<style>
.block-container { padding-top: 1.25rem; }
.stChatMessage { border-radius: 12px; padding: 0.6rem 0.9rem; }
.user-msg { background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.15); }
.assistant-msg { background: rgba(59, 130, 246, 0.05); border: 1px solid rgba(59, 130, 246, 0.12); }
.feedback-msg { background: rgba(244, 114, 182, 0.06); border: 1px solid rgba(244, 114, 182, 0.12); font-style: italic; }
.smalltext { font-size: 0.85rem; color: #6b7280; }
h1 span.badge {
    background: linear-gradient(90deg, #10b981, #3b82f6);
    color: white; border-radius: 0.5rem; padding: 0.15rem 0.5rem; font-size: 0.7em; margin-left: 0.5rem;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------#
# -------   Sidebar UI  -------#
# -----------------------------#
init_session_state()

with st.sidebar:
    st.header("⚙️ Controls")

    st.session_state.success_criteria = st.text_area(
        "Success Criteria",
        value=st.session_state.success_criteria,
        height=140,
        help="Tell Visexa Pilot what 'done' looks like. The evaluator will use this.",
    )

    st.session_state.disable_tracing = st.toggle(
        "Disable LangSmith tracing (dev mode)",
        value=st.session_state.disable_tracing,
        help="Turn off tracing to avoid clutter & ghost runs while debugging.",
    )

    st.caption("Playwright is forced to headless=True via env var PLAYWRIGHT_HEADLESS.")

    st.divider()
    if st.button("🔁 Reset Conversation", use_container_width=True, type="secondary"):
        reset_everything()

# -----------------------------#
# -------  Main Screen  -------#
# -----------------------------#
st.title("Visexa Pilot")
st.caption("A LangGraph + Tool-using, self-reflecting agent that iterates until it meets your success criteria.")

# Make sure sidekick is ready
setup_sidekick()

# ------- Render past messages -------
def render_history():
    for m in st.session_state.history:
        role = m.get("role", "assistant")
        css_class = (
            "user-msg" if role == "user"
            else "feedback-msg" if "Evaluator Feedback" in m.get("content", "")
            else "assistant-msg"
        )
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(f"<div class='{css_class}'>{m['content']}</div>", unsafe_allow_html=True)

render_history()

# ------- Chat input -------
prompt = st.chat_input("Ask Visexa Pilot anything…")

if prompt:
    # 1) Show user message instantly
    with st.chat_message("user"):
        st.markdown(f"<div class='user-msg'>{prompt}</div>", unsafe_allow_html=True)

    # 2) Call Sidekick
    with st.spinner("Visexa Pilot is thinking…"):
        try:
            updated_history = run_async(
                st.session_state.sidekick.run_superstep(
                    prompt,
                    st.session_state.success_criteria,
                    st.session_state.history,
                )
            )
            st.session_state.history = updated_history
        except Exception as e:
            st.error(f"Something went wrong: {e}")

    st.rerun()

st.markdown(
    "<p class='smalltext'>Tip: Edit the success criteria above to force the agent to iterate until your bar is met.</p>",
    unsafe_allow_html=True,
)
