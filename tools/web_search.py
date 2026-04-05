"""Web search tool — used by the research subagent to search the internet."""

from ddgs import DDGS
from config import MAX_SEARCH_RESULTS


def web_search(query: str, max_results: int = 5) -> str:
    """Search the web for a given query and return results with titles, URLs, and snippets.

    Args:
        query: The search query string.
        max_results: Maximum number of results to return.
    """
    ddgs = DDGS()
    results = ddgs.text(query, max_results=max_results or MAX_SEARCH_RESULTS)

    if not results:
        return f"No results found for: {query}"

    output = ""
    for r in results:
        title = r.get("title", "")
        url = r.get("href", "")
        body = r.get("body", "")
        output += f"**{title}**\n{url}\n{body}\n\n"

    return output
