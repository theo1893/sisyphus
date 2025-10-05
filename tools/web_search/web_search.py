import json
from typing import Annotated

from loguru import logger
from tavily import TavilyClient

from tools.util import sisyphus_register, sisyphus_tool


class WebSearchTool:
    api_key: str
    tavily_client: TavilyClient

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.tavily_client = TavilyClient(api_key=self.api_key)
        sisyphus_register(self)

    @sisyphus_tool
    def web_search(self,
                   query: Annotated[
                       str, "The search query to find relevant web pages. Be specific and include key terms to improve search accuracy. For best results, use natural language questions or keyword combinations that precisely describe what you're looking for."],
                   num_results: Annotated[
                       int, "The number of search results to return. Increase for more comprehensive research or decrease for focused, high-relevance results."] = 20,
                   ):
        """
        Search the web using the Tavily API to find relevant and up-to-date information.
        """

        logger.info(f"Executing web search for query: '{query}' with {num_results} results")
        search_response = self.tavily_client.search(
            query=query,
            max_results=num_results,
            include_images=True,
            include_answer="advanced",
            search_depth="advanced",
        )

        results = search_response.get('results', [])
        answer = search_response.get('answer', '')

        logger.info(f"Retrieved search results for query: '{query}' with answer and {len(results)} results")

        if len(results) > 0 or (answer and answer.strip()):
            return json.dumps(search_response, ensure_ascii=False)
        else:
            return f"No search results or answer found for query: '{query}'"
