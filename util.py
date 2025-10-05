from typing import List, Union, Literal

from langchain_core.messages import BaseMessage, ToolMessage, AIMessage, HumanMessage
from langchain_core.messages.utils import count_tokens_approximately


def compress_messages(messages: List[BaseMessage], max_tokens: int, single_msg_threshold: int,
                      target: Union[str, Literal["tool", "ai", "human"]]) -> List[
    BaseMessage]:
    uncompressed_total_token_count = count_tokens_approximately(messages=messages)
    max_tokens_value = max_tokens or (100 * 1000)

    if uncompressed_total_token_count > max_tokens_value:
        _i = 0
        for msg in reversed(messages):
            if target == "tool":
                cls = ToolMessage
            if target == "ai":
                cls = AIMessage
            if target == "human":
                cls = HumanMessage

            if isinstance(msg, cls):
                _i += 1
                msg_token_count = count_tokens_approximately(messages=[msg])
                if msg_token_count > single_msg_threshold:
                    if _i > 1:
                        compressed_msg = compress_message(msg, msg.id, single_msg_threshold * 3)
                    else:
                        compressed_msg = safe_truncate(msg, int(max_tokens_value * 2))
                    msg.content = compressed_msg.content
    return messages


def safe_truncate(msg: BaseMessage, max_length: int = 100000) -> BaseMessage:
    max_length = min(max_length, 100000)

    if len(msg.content) > max_length:
        keep_length = max_length - 150
        start_length = keep_length // 2
        end_length = keep_length - start_length

        start_part = msg.content[:start_length]
        end_part = msg.content[-end_length:] if end_length > 0 else ""

        truncated_content = start_part + f"\n\n... (middle truncated) ...\n\n" + end_part + f"\n\nThis message is too long, repeat relevant information in your response to remember it"
        msg.content = truncated_content

    return msg


def compress_message(msg: BaseMessage, message_id: str, max_length: int = 3000) -> BaseMessage:
    if len(msg.content) > max_length:
        compressed_content = msg.content[
                             :max_length] + "... (truncated)" + f"\n\nmessage_id \"{message_id}\"\nUse expand-message tool to see contents"
        msg.content = compressed_content

    return msg