from dataclasses import dataclass

from langchain_core.tools import tool

from tools import tool_registry


def sisyphus_register(instance):
    for attr_name in dir(instance):
        attr = getattr(instance, attr_name)

        if hasattr(attr, '__sisyphus_tool__'):
            raw_tool = tool(attr)
            tool_registry.register(raw_tool)


def sisyphus_tool(func):
    func.__sisyphus_tool__ = True
    return func


@dataclass
class ToolResult:
    success: bool
    output: str
