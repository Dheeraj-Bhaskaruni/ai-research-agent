---
title: Research Agent System
emoji: ""
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.56.0"
app_file: app.py
pinned: true
license: mit
short_description: Deep multi-agent research pipeline with LangGraph
---

# Research Agent System

A multi-agent pipeline that researches any topic end-to-end. Built with Deep Agents, LangChain, LangGraph, and LangSmith.

An orchestrator agent plans the work, then delegates to 4 specialized subagents — each with isolated context, their own planning, and tool access. If the reviewer says "REVISE", the writer automatically rewrites.

## Architecture

```
Orchestrator (plans + delegates)
|
+-- Researcher
|   - Generates search queries
|   - Searches the web (DuckDuckGo)
|   - Compiles findings into a brief
|
+-- Analyzer
|   - Extracts top 5 insights
|   - Finds patterns and contradictions
|
+-- Writer
|   - Produces polished report
|   - Executive summary, findings, recommendations
|
+-- Reviewer
    - Scores on 4 criteria (1-10)
    - Verdict: PASS or REVISE
    - REVISE loops back to Writer
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Framework | Deep Agents |
| Orchestration | LangGraph |
| LLM Framework | LangChain |
| LLM | OpenAI GPT-4o-mini (configurable) |
| Web Search | DuckDuckGo (free, no API key) |
| Observability | LangSmith |
| Frontend | Streamlit |
| Language | Python 3.10+ |

## Setup

```bash
git clone https://github.com/Dheeraj-Bhaskaruni/ai-research-agent.git
cd ai-research-agent
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Usage

### CLI
```bash
python main.py "The future of AI agents in 2025"
python main.py  # Interactive prompt
```

### Web UI
```bash
streamlit run app.py
```

## LangSmith Setup (Optional, Free)

LangSmith traces every LLM call, tool invocation, and subagent step.

1. Create account at [smith.langchain.com](https://smith.langchain.com)
2. Settings > API Keys > Create Key
3. Add to `.env`:
   ```
   LANGSMITH_API_KEY=lsv2_pt_xxxxx
   LANGSMITH_TRACING=true
   ```

## Deploy to Hugging Face Spaces

1. Create a new Space at [huggingface.co/new-space](https://huggingface.co/new-space) (SDK: Streamlit)
2. Push the code:
   ```bash
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/ai-research-agent
   git push hf main
   ```
3. Add secrets in Space Settings:
   - `OPENAI_API_KEY`
   - `LANGSMITH_API_KEY` (optional)
   - `LANGSMITH_TRACING` = `true` (optional)

## Project Structure

```
ai-research-agent/
├── agent.py              # Orchestrator + 4 subagent definitions
├── tools/
│   └── web_search.py     # DuckDuckGo search tool
├── app.py                # Streamlit frontend
├── main.py               # CLI entry point
├── config.py             # Environment config
├── requirements.txt
├── .env.example
└── README.md
```

## Deployment Options

| Platform | Type | Cost | Notes |
|----------|------|------|-------|
| **Hugging Face Spaces** | Streamlit hosting | Free | Best for demos/portfolio |
| **Streamlit Cloud** | Streamlit hosting | Free | Direct GitHub integration |
| **Railway** | Container hosting | $5/mo | Custom domain, auto-deploy |
| **Render** | Container hosting | Free tier | Good for side projects |
| **AWS/GCP/Azure** | Full cloud | Pay-as-you-go | Production scale |
| **Docker** | Self-hosted | Free | Run anywhere |

## License

MIT
