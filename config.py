import os

# Load .env for local development (ignored on HF Spaces)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not needed on HF Spaces — secrets come from env

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL", "gpt-4o-mini")

# LangSmith
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "ai-research-agent")
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "false")

# Search
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))


def setup_langsmith():
    """Activate LangSmith tracing if configured."""
    if LANGSMITH_API_KEY and LANGSMITH_TRACING.lower() == "true":
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = LANGSMITH_API_KEY
        os.environ["LANGCHAIN_PROJECT"] = LANGSMITH_PROJECT
        return True
    return False
