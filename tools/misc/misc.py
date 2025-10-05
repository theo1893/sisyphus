from typing import Annotated

import requests
from loguru import logger

from storage import storage
from tools.util import sisyphus_register, sisyphus_tool


class MiscTool:
    def __init__(self):
        sisyphus_register(self)

    @sisyphus_tool
    def expand_message(self, message_id: Annotated[str, "The ID of the message to expand."]):
        """Expand a message from the previous conversation with the user. Use this tool to expand a message that was truncated in the earlier conversation."""
        message = storage.get_value(message_id)
        if message:
            return message
        else:
            return f"The message for {message_id} is empty"

    @sisyphus_tool
    def ask(self,
            text: Annotated[
                str, "Question text to present to user - should be specific and clearly indicate what information you need. Use natural, conversational language. Include: 1) Clear question or request, 2) Context about why the input is needed, 3) Available options if applicable, 4) Impact of different choices, 5) Any relevant constraints or considerations."],
            ):
        """
        Ask user a question and wait for response. Use for:
        1) Requesting clarification on ambiguous requirements,
        2) Seeking confirmation before proceeding with high-impact changes,
        3) Gathering additional information needed to complete a task,
        4) Offering options and requesting user preference,
        5) Validating assumptions when critical to task success,
        6) When encountering unclear or ambiguous results during task execution,
        7) When tool results don't match expectations,
        8) For natural conversation and follow-up questions,
        9) When research reveals multiple entities with the same name,
        10) When user requirements are unclear or could be interpreted differently.
        IMPORTANT: Use this tool when user input is essential to proceed. Always provide clear context and options when applicable. Use natural, conversational language that feels like talking with a helpful friend. CRITICAL: When you discover ambiguity (like multiple people with the same name), immediately stop and ask for clarification rather than making assumptions.
        """
        response = input(text)
        return response

    @sisyphus_tool
    def browser_takeover(self, text: Annotated[
        str, "Instructions for the user about what actions to take in the browser. Include: 1) Clear explanation of why takeover is needed, 2) Specific steps the user should take, 3) What information to look for or extract, 4) How to indicate when they're done, 5) Any important context about the current page state."]):
        """
        Request user takeover of browser interaction. Use this tool when:
        1) The page requires complex human interaction that automated tools cannot handle,
        2) Authentication or verification steps require human input,
        3) The page has anti-bot measures that prevent automated access,
        4) Complex form filling or navigation is needed,
        5) The page requires human verification (CAPTCHA, etc.).
        IMPORTANT: This tool should be used as a last resort after web-search and crawl-webpage have failed, and when direct browser tools are insufficient. Always provide clear context about why takeover is needed and what actions the user should take.
        """
        input(f"{text}\nPress enter to continue...")

        ## 获取用户介入后的浏览器状态
        url = f"http://localhost:8000/api/automation/get_browser_state"
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.get(url, params={}, headers=headers, timeout=30)

        response.raise_for_status()
        logger.debug("Browser automation request completed successfully")

        return response.text
