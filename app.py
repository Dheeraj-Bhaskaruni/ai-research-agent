"""Streamlit frontend for the AI Research Agent System (Deep Agents)."""

import os
import streamlit as st
from config import setup_langsmith, LANGSMITH_API_KEY, LANGSMITH_TRACING, LANGSMITH_PROJECT

# Activate LangSmith
tracing = setup_langsmith()

from agent import build_agent

st.set_page_config(
    page_title="AI Research Agent (Deep Agents)",
    page_icon="🔬",
    layout="wide",
)

st.title("🔬 AI Research Agent System")
st.caption("Powered by Deep Agents + LangChain + LangGraph + LangSmith")

# Sidebar
with st.sidebar:
    st.header("Deep Agent Architecture")
    st.markdown("""
    ```
    🧠 Orchestrator (Deep Agent)
    │  Plans with write_todos
    │  Delegates via task tool
    │
    ├── 🔍 Researcher (subagent)
    │   Uses web_search, plans own work
    │
    ├── 🧠 Analyzer (subagent)
    │   Extracts insights & patterns
    │
    ├── ✍️ Writer (subagent)
    │   Produces polished report
    │
    └── 📋 Reviewer (subagent)
        Scores & gives PASS/REVISE
        → loops back to Writer if REVISE
    ```

    **What makes it "deep":**
    - Built-in task planning (todos)
    - Subagent delegation (isolated context)
    - File system access (persistent output)
    - Auto context summarization
    """)

    st.divider()

    langsmith_status = "🟢 ON" if tracing else "🔴 OFF"
    st.markdown(f"**LangSmith Tracing:** {langsmith_status}")
    if tracing:
        st.markdown(f"Project: `{LANGSMITH_PROJECT}`")
        st.markdown("[Open LangSmith Dashboard →](https://smith.langchain.com)")

    st.divider()
    st.markdown("**Tech Stack:** Deep Agents, LangChain, LangGraph, LangSmith, OpenAI, Streamlit")

# Main input
topic = st.text_input(
    "Research Topic",
    placeholder="e.g., The impact of AI agents on software development in 2025",
)

if st.button("🚀 Start Deep Research", type="primary", disabled=not topic):
    agent = build_agent()

    progress = st.progress(0, text="Starting deep agent pipeline...")
    activity_log = st.expander("Agent Activity Log", expanded=True)
    log_container = activity_log.empty()
    log_lines = []

    def add_log(line: str):
        log_lines.append(line)
        log_container.markdown("\n".join(log_lines))

    add_log("🚀 **Pipeline started**")

    # Stream and collect final result
    step_count = 0
    total_steps = 20
    final_content = ""

    for event in agent.stream(
        {"messages": [{"role": "user", "content": f"Research this topic thoroughly and produce a full report: {topic}"}]},
        stream_mode="updates",
    ):
        if not isinstance(event, dict):
            continue

        step_count += 1
        progress.progress(min(step_count / total_steps, 0.95), text="Deep agent working...")

        for node_name, node_data in event.items():
            if not isinstance(node_data, dict):
                continue

            messages = node_data.get("messages")
            if messages is None:
                continue

            if hasattr(messages, "value"):
                messages = messages.value

            if not isinstance(messages, list):
                continue

            for msg in messages:
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tc in msg.tool_calls:
                        name = tc.get("name", "")
                        args = tc.get("args", {})
                        if name == "task":
                            agent_name = args.get("agent", args.get("name", "unknown"))
                            add_log(f"📋 **Delegating to:** `{agent_name}`")
                        elif name == "write_todos":
                            add_log("📝 **Planning tasks...**")
                        elif name == "web_search":
                            query = args.get("query", "")
                            add_log(f"🔍 **Searching:** `{query}`")
                        elif name == "write_file":
                            path = args.get("path", "")
                            add_log(f"💾 **Saving file:** `{path}`")

                if hasattr(msg, "content") and msg.content and not getattr(msg, "tool_calls", None):
                    if len(msg.content) > 100:
                        final_content = msg.content
                        add_log(f"✅ **{node_name}** completed")

    progress.progress(1.0, text="Done!")
    add_log("🎉 **Pipeline complete!**")

    # Display final report
    st.divider()
    st.subheader("📄 Final Report")

    if final_content:
        st.markdown(final_content)
        st.download_button(
            label="📥 Download Report",
            data=final_content,
            file_name=f"{topic[:30].replace(' ', '_')}_report.md",
            mime="text/markdown",
        )
    else:
        st.warning("No report generated. Check LangSmith for details.")
