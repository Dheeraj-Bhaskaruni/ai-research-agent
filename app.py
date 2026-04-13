"""Streamlit frontend for the Research Agent System."""

import os
import streamlit as st
from config import setup_langsmith, LANGSMITH_API_KEY, LANGSMITH_TRACING, LANGSMITH_PROJECT

tracing = setup_langsmith()

from agent import build_agent

st.set_page_config(
    page_title="Research Agent",
    page_icon="",
    layout="wide",
)

st.title("Research Agent System")
st.caption("Multi-agent research pipeline built with LangGraph")

# Sidebar
with st.sidebar:
    st.header("Architecture")
    st.markdown("""
    **Pipeline Flow:**

    ```
    Orchestrator (plans + delegates)
    |
    +-- Researcher (web search)
    +-- Analyzer (insights)
    +-- Writer (report)
    +-- Reviewer (quality check)
        |-- REVISE -> Writer
        |-- PASS -> Done
    ```

    **Key Features:**
    - Task planning at every level
    - Subagent delegation with isolated context
    - Live web search (DuckDuckGo)
    - Automatic revision loop
    - Full observability via LangSmith
    """)

    st.divider()

    langsmith_status = "Active" if tracing else "Inactive"
    st.markdown(f"**Tracing:** {langsmith_status}")
    if tracing:
        st.markdown(f"Project: `{LANGSMITH_PROJECT}`")
        st.markdown("[Open Dashboard](https://smith.langchain.com)")

    st.divider()
    st.markdown("**Stack:** Deep Agents, LangChain, LangGraph, LangSmith, OpenAI, Streamlit")

# Main input
topic = st.text_input(
    "Research Topic",
    placeholder="e.g., The impact of AI agents on software development in 2025",
)

if st.button("Start Research", type="primary", disabled=not topic):
    agent = build_agent()

    progress = st.progress(0, text="Starting pipeline...")
    activity_log = st.expander("Activity Log", expanded=True)
    log_container = activity_log.empty()
    log_lines = []

    def add_log(line: str):
        log_lines.append(line)
        log_container.markdown("\n".join(log_lines))

    add_log("**Pipeline started**")

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
        progress.progress(min(step_count / total_steps, 0.95), text="Working...")

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
                            add_log(f"**Delegating to:** `{agent_name}`")
                        elif name == "write_todos":
                            add_log("**Planning tasks...**")
                        elif name == "web_search":
                            query = args.get("query", "")
                            add_log(f"**Searching:** `{query}`")
                        elif name == "write_file":
                            path = args.get("path", "")
                            add_log(f"**Saving:** `{path}`")

                if hasattr(msg, "content") and msg.content and not getattr(msg, "tool_calls", None):
                    if len(msg.content) > 100:
                        final_content = msg.content
                        add_log(f"**{node_name}** completed")

    progress.progress(1.0, text="Done")
    add_log("**Pipeline complete**")

    # Display final report
    st.divider()
    st.subheader("Final Report")

    if final_content:
        st.markdown(final_content)
        st.download_button(
            label="Download Report",
            data=final_content,
            file_name=f"{topic[:30].replace(' ', '_')}_report.md",
            mime="text/markdown",
        )
    else:
        st.warning("No report generated. Check LangSmith for details.")
