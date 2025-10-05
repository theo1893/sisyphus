import os

from tools.web_search.web_search import WebSearchTool


def initialize():
    _ = WebSearchTool(api_key=os.getenv("TAVILY_API_KEY"))
