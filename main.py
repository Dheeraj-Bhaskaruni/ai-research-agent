#!/usr/bin/env python3
"""CLI entry point for the AI Research Agent System (Deep Agents).

Usage:
    python main.py "Your research topic here"
    python main.py   # Interactive prompt
"""

import sys
from config import setup_langsmith

# Activate LangSmith tracing if configured
tracing = setup_langsmith()

from agent import build_agent


def main():
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("\nEnter your research topic: ").strip()
        if not topic:
            print("Error: Please provide a topic.")
            sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  Research Agent System")
    print(f"  Topic: {topic}")
    if tracing:
        print(f"  Tracing: ON")
    print(f"{'='*60}")
    print("\nStarting pipeline...\n")

    agent = build_agent()

    # Stream and collect the final result in one pass
    final_content = ""

    for event in agent.stream(
        {"messages": [{"role": "user", "content": f"Research this topic thoroughly and produce a full report: {topic}"}]},
        stream_mode="updates",
    ):
        if not isinstance(event, dict):
            continue

        for node_name, node_data in event.items():
            if not isinstance(node_data, dict):
                continue

            messages = node_data.get("messages")
            if messages is None:
                continue

            # Handle Overwrite wrapper
            if hasattr(messages, "value"):
                messages = messages.value

            if not isinstance(messages, list):
                continue

            for msg in messages:
                # Show tool calls
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tc in msg.tool_calls:
                        name = tc.get("name", "")
                        args = tc.get("args", {})
                        if name == "task":
                            agent_name = args.get("agent", args.get("name", "unknown"))
                            task_desc = args.get("description", "")[:80]
                            print(f"  [delegating] {agent_name}")
                            if task_desc:
                                print(f"     → {task_desc}")
                        elif name == "write_todos":
                            print(f"  [planning]")
                        elif name == "web_search":
                            query = args.get("query", "")
                            print(f"  [searching] {query}")
                        elif name == "write_file":
                            path = args.get("path", "")
                            print(f"  [saving] {path}")

                # Capture final AI response
                if hasattr(msg, "content") and msg.content and not getattr(msg, "tool_calls", None):
                    if len(msg.content) > 100:
                        final_content = msg.content

    print(f"\n{'='*60}")
    print("  FINAL REPORT")
    print(f"{'='*60}\n")

    if final_content:
        print(final_content)

        # Save report
        filename = topic.lower().replace(" ", "_")[:50] + "_report.md"
        with open(filename, "w") as f:
            f.write(f"# Research Report: {topic}\n\n")
            f.write(final_content)
        print(f"\nReport saved to: {filename}")
    else:
        print("No report generated. Check LangSmith for details.")


if __name__ == "__main__":
    main()
