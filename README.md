---
title: AI Research Agent System
emoji: 🔬
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.56.0"
app_file: app.py
pinned: true
license: mit
short_description: Deep multi-agent AI research pipeline with LangGraph
---

# 🔬 AI Research Agent System (Deep Agents)

A **deep multi-agent AI pipeline** that researches any topic end-to-end. Built with **Deep Agents**, **LangChain**, **LangGraph**, and **LangSmith**.

An orchestrator agent plans the work, then delegates to 4 specialized subagents — each with isolated context, their own planning, and tool access. If the reviewer says "REVISE", the writer automatically rewrites.

## Why "Deep" Agents?

Most AI agent tutorials build "shallow" agents — simple tool-calling loops that break on complex tasks. **Deep agents** add:

| Feature | Shallow Agent | Deep Agent (this project) |
|---------|:---:|:---:|
| Task planning (todos) | No | Yes |
| Subagent delegation | No | Yes (4 specialists) |
| Isolated context per agent | No | Yes |
| File system access | No | Yes |
| Auto context summarization | No | Yes |
| Revision loops | No | Yes |

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    🧠 ORCHESTRATOR                            │
│              (Deep Agent with planning + delegation)          │
│                                                              │
│   1. Plans with write_todos                                  │
│   2. Delegates via task tool to subagents:                   │
│                                                              │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│   │ 🔍 Researcher│  │ 🧠 Analyzer  │  │ ✍️ Writer    │      │
│   │  - web_search│  │  - insights  │  │  - report    │      │
│   │  - planning  │  │  - patterns  │  │  - structure │      │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│          │                 │                  │     ▲         │
│          ▼                 ▼                  ▼     │         │
│      Research brief → Analysis report → Final report         │
│                                               │              │
│                                        ┌──────┴───────┐      │
│                                        │ 📋 Reviewer  │      │
│                                        │  - scores    │      │
│                                        │  - PASS/     │      │
│                                        │    REVISE    │      │
│                                        └──────────────┘      │
│                                                              │
│   ┌──────────────────────────────────────────────────────┐   │
│   │  LangSmith Tracing — every LLM call, tool call,     │   │
│   │  subagent spawn, and planning step is traced         │   │
│   └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Agent Framework** | Deep Agents (`deepagents`) |
| **Orchestration** | LangGraph (state graph, under the hood) |
| **LLM Framework** | LangChain |
| **LLM** | OpenAI GPT-4o-mini (configurable) |
| **Web Search** | DuckDuckGo (free, no API key) |
| **Observability** | LangSmith (full pipeline tracing) |
| **Frontend** | Streamlit |
| **Language** | Python 3.10+ |

## Setup

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd ai-research-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env → add your OPENAI_API_KEY
```

## Usage

### CLI
```bash
python main.py "The future of AI agents in 2025"
python main.py  # Interactive prompt
```

### Web UI (Streamlit)
```bash
streamlit run app.py
```

## Setting Up LangSmith (Free)

LangSmith traces every LLM call, tool invocation, subagent spawn, and planning step.

1. Go to [smith.langchain.com](https://smith.langchain.com) → create free account
2. **Settings** → **API Keys** → **Create API Key**
3. Add to `.env`:
   ```
   LANGSMITH_API_KEY=lsv2_pt_xxxxx
   LANGSMITH_TRACING=true
   ```
4. Run the app — traces show up automatically with:
   - Full pipeline execution timeline
   - Input/output of every subagent
   - Token usage and latency per step
   - Tool call details (search queries, results)
   - Planning steps (todos created by each agent)

## Project Structure

```
ai-research-agent/
├── agent.py               # Deep agent setup — orchestrator + 4 subagents
├── tools/
│   ├── __init__.py
│   └── web_search.py      # DuckDuckGo search tool
├── app.py                 # Streamlit web frontend
├── main.py                # CLI entry point
├── config.py              # Environment + LangSmith config
├── requirements.txt
├── .env.example
└── README.md
```

## How It Works (Step by Step)

1. **User** enters a topic
2. **Orchestrator** creates a plan using `write_todos`
3. **Orchestrator** spawns `researcher` subagent via `task` tool
4. **Researcher** creates its own plan, runs multiple `web_search` calls, compiles a brief
5. **Orchestrator** spawns `analyzer` subagent with the research brief
6. **Analyzer** creates its plan, extracts insights, patterns, contradictions
7. **Orchestrator** spawns `writer` subagent with research + analysis
8. **Writer** creates its plan, produces a polished report
9. **Orchestrator** spawns `reviewer` subagent with the report
10. **Reviewer** scores the report on 4 criteria, gives PASS/REVISE
11. If **REVISE** → writer gets feedback and rewrites. If **PASS** → done!
12. **Orchestrator** saves final report and presents to user

## Key Design Decisions

1. **Deep Agents over raw LangGraph** — Gets planning, subagents, file tools, and summarization for free. Production-grade agent patterns without boilerplate.
2. **Subagent isolation** — Each agent has its own context window. The researcher doesn't pollute the writer's context with raw search results.
3. **Planning at every level** — Both the orchestrator AND each subagent plan their work with `write_todos`. This is what makes complex tasks reliable.
4. **Revision loop** — The reviewer can trigger rewrites, demonstrating dynamic agent workflow.
5. **Free web search** — DuckDuckGo requires no API key.

## Deploy to Hugging Face Spaces

This app is ready for Hugging Face Spaces (Streamlit).

### Step-by-step:

1. **Create a Hugging Face account** at [huggingface.co](https://huggingface.co)

2. **Create a new Space:**
   - Go to [huggingface.co/new-space](https://huggingface.co/new-space)
   - Name: `ai-research-agent`
   - SDK: **Streamlit**
   - Visibility: Public (or Private)
   - Click **Create Space**

3. **Push the code:**
   ```bash
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/ai-research-agent
   git push hf main
   ```

4. **Add your API keys as Secrets** (not in code!):
   - Go to your Space → **Settings** → **Variables and secrets**
   - Add these secrets:
     - `OPENAI_API_KEY` = `sk-proj-...`
     - `LANGSMITH_API_KEY` = `lsv2_pt_...` (optional)
     - `LANGSMITH_TRACING` = `true` (optional)

5. The app will build automatically and be live at:
   ```
   https://huggingface.co/spaces/YOUR_USERNAME/ai-research-agent
   ```

## Extending

- **Add more subagents**: Define a new `SubAgent` dict in `agent.py`
- **Add tools**: Write a function with type hints + docstring, add to tools list
- **Change model**: Set `MODEL=gpt-4o` in `.env` for better quality
- **Add persistence**: Pass a `checkpointer` to `create_deep_agent()` for conversation memory
- **Deploy**: Containerize with Docker, deploy to Railway/Render/AWS

## Interview Talking Points

- "I built a deep agent system with planning, subagent delegation, and a revision loop"
- "Each agent has isolated context — this prevents context pollution in long tasks"
- "The orchestrator plans before delegating, and each subagent plans its own subtasks"
- "LangSmith traces every step — I can debug any agent's behavior in production"
- "The architecture follows the same patterns as Claude Code and Deep Research"

## License

MIT
