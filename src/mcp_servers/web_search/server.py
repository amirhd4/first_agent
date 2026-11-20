from ddgs import DDGS
from mcp.server import MCPServer

mcp = MCPServer("web-search-mcp")


@mcp.tool()
def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    Search the internet for up-to-date information, articles, and answers.

    Args:
        query: The search query string.
        max_results: Maximum number of results to return (default is 5).
    """
    results = []
    try:
        with DDGS() as ddgs:
            search_results = ddgs.text(query, max_results=max_results)
            for item in search_results:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("href", ""),
                    "snippet": item.get("body", ""),
                })
    except Exception as e:
        return [{"error": f"Search failed: {str(e)}"}]

    return results


@mcp.tool()
def search_news(query: str, max_results: int = 5) -> list[dict]:
    """
    Search recent news articles on the internet.

    Args:
        query: The news topic or keywords to search for.
        max_results: Maximum number of news items to return (default is 5).
    """
    results = []
    try:
        with DDGS() as ddgs:
            news_results = ddgs.news(query, max_results=max_results)
            for item in news_results:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "date": item.get("date", ""),
                    "source": item.get("source", ""),
                    "snippet": item.get("body", ""),
                })
    except Exception as e:
        return [{"error": f"News search failed: {str(e)}"}]

    return results


if __name__ == "__main__":
    mcp.run()