
from ddgs import DDGS


def search_documentation(query: str, max_results: int = 5) -> dict:
    """Search the web for documentation and return real search results."""
    query = query.strip()

    if not query:
        return {"error": "Search query cannot be empty", "results": []}

    try:
        results = DDGS().text(query, max_results=max_results)

        items = [
            {
                "title": item.get("title", ""),
                "url": item.get("href", ""),
                "snippet": item.get("body", ""),
            }
            for item in results
        ]

        return {"query": query, "results": items, "count": len(items)}

    except Exception as exc:
        return {
            "error": f"{type(exc).__name__}: {exc}",
            "results": [],
        }
