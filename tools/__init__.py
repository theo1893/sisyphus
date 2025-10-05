from typing import List

from langchain_core.tools import BaseTool


class ToolRegistry:
    tools: List[BaseTool]

    # registry: Dict[str, any]

    def __init__(self):
        self.tools = []
        # self.registry = {}

    def register(self, tool: BaseTool):
        self.tools.append(tool)
        # self.registry[tool.name] = instance


tool_registry = ToolRegistry()

# __all__ = ["tool_registry", "browser", "file", "data_provider", "misc", "shell", "task", "web_search"]
