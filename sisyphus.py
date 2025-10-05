import os
import sys
from typing import cast

from dotenv import load_dotenv

from prompt.prompt import SYSTEM_PROMPT
from util import compress_messages

load_dotenv()

from storage import storage

from tools import (browser, data_provider, file, misc, shell, task, web_search)
from loguru import logger
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langgraph.constants import END
from langgraph.graph import StateGraph, MessagesState
from langchain_core.messages import AIMessage, HumanMessage, ToolCall, SystemMessage
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode
from langgraph.types import Command

from tools import tool_registry


class State(MessagesState):
    current_step: int
    max_step: int
    tool_calls: list[ToolCall]


class Sisyphus:
    state: State
    graph: CompiledStateGraph

    def __init__(self, max_step: int, graph: CompiledStateGraph):
        self.graph = graph
        self.state: State = State(
            current_step=0,
            max_step=max_step,
            messages=[SystemMessage(SYSTEM_PROMPT)]
        )

    def __call__(self, query: str):
        self.state["messages"].append(HumanMessage(query))

        self.graph.invoke(self.state, {"recursion_limit": 65535})


def gen_graph(model: str) -> CompiledStateGraph:
    tool_node = ToolNode(tools=tool_registry.tools)
    tool_classes = list(tool_node.tools_by_name.values())
    model = cast(BaseChatModel, init_chat_model(model)).bind_tools(tool_classes)

    def acting_node(state: State):
        logger.info(f"Acting for step {state['current_step']}")
        response = tool_node.invoke(state)
        logger.info(f"Acting result:\n {response['messages'][-1]}")

        return Command(
            goto="reasoning_node",
            update={"messages": response['messages'], "current_step": state["current_step"] + 1},
        )

    def reasoning_node(state: State):
        latest_msg = state["messages"][-1]
        if not isinstance(latest_msg, SystemMessage):
            storage.set_value(latest_msg.id, latest_msg)

        if state["current_step"] == state["max_step"]:
            logger.warning("run out of steps")
            return Command(
                goto=END,
                update={},
            )

        logger.info(f"Reasoning for step {state['current_step']}")

        messages = state["messages"]
        messages = compress_messages(messages=messages, max_tokens=12800, single_msg_threshold=1024, target="tool")
        messages = compress_messages(messages=messages, max_tokens=12800, single_msg_threshold=1024, target="human")
        messages = compress_messages(messages=messages, max_tokens=12800, single_msg_threshold=1025, target="ai")

        prompt = ChatPromptTemplate.from_messages(messages).invoke({})
        response = cast(AIMessage, model.invoke(prompt))
        logger.info(f"Reasoning result:\n {response.content}")
        storage.set_value(response.id, latest_msg)

        if not response.tool_calls:
            return Command(
                goto=END,
                update={},
            )
        else:
            return Command(
                goto="acting_node",
                update={"messages": [response]},
            )

    builder = StateGraph(state_schema=State)
    builder.add_node("reasoning_node", reasoning_node)
    builder.add_node("acting_node", acting_node)
    builder.add_edge("acting_node", "reasoning_node")

    builder.set_entry_point("reasoning_node")
    graph = builder.compile()

    return graph


def gen_sisyphus(max_step=25) -> Sisyphus:
    graph = gen_graph(os.getenv("MODEL"))

    return Sisyphus(
        graph=graph,
        max_step=max_step,
    )


def initialize():
    # Remove default logger to customize it
    logger.remove()
    
    # Add human-friendly logger with colors and better formatting
    logger.add(
        lambda msg: print(msg, end=""),  # Output to console
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # Also add a file logger for debugging (without colors)
    logger.add(
        "sisyphus.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
        compression="zip"
    )

    browser.initialize()
    file.initialize()
    data_provider.initialize()
    misc.initialize()
    shell.initialize()
    task.initialize()
    web_search.initialize()


if __name__ == "__main__":
    initialize()
    
    # Check if query is provided as command line arguments
    if len(sys.argv) < 2:
        logger.error("Usage: python sisyphus.py <query>")
        logger.info("Example: python sisyphus.py 'What is the weather today?'")
        sys.exit(1)
    
    # Join all arguments after the script name as the query
    query = " ".join(sys.argv[1:])
    logger.info(f"Received query: {query}")
    
    sisyphus = gen_sisyphus(max_step=100)
    sisyphus(query)
