from typing import Annotated

import requests
from loguru import logger
from playwright.sync_api import Browser, BrowserContext, Page

from tools.browser.cls import *
from tools.util import sisyphus_tool, sisyphus_register


class BrowserTool:
    browser: Browser = None
    browser_context: BrowserContext = None
    pages: List[Page] = []
    current_page_index: int = 0
    include_attributes = ["id", "href", "src", "alt", "aria-label", "placeholder", "name", "role", "title",
                          "value"]

    def __init__(self):
        sisyphus_register(self)

    @sisyphus_tool
    def browser_navigate_to(self, url: Annotated[str, "The url to navigate to"]) -> str:
        """Navigate to a specific url

        Args:
            url (str): The url to navigate to

        Returns:
            dict: Result of the execution
        """
        return self._execute_browser_action("navigate_to", {"url": url})

    @sisyphus_tool
    def browser_go_back(self) -> str:
        """Navigate back in browser history

        Returns:
            dict: Result of the execution
        """
        logger.debug(f"Navigating back in browser history\033[0m")
        return self._execute_browser_action("go_back", {})

    @sisyphus_tool
    def browser_wait(self, seconds: int = 3) -> str:
        """Wait for the specified number of seconds

        Args:
            seconds (int, optional): Number of seconds to wait. Defaults to 3.

        Returns:
            dict: Result of the execution
        """
        logger.debug(f"Waiting for {seconds} seconds\033[0m")
        return self._execute_browser_action("wait", {"seconds": seconds})

    @sisyphus_tool
    def browser_click_element(self, index: Annotated[int, "The index of the element to click"]) -> str:
        """Click on an element by index

        Args:
            index (int): The index of the element to click

        Returns:
            dict: Result of the execution
        """
        logger.debug(f"Clicking element with index: {index}\033[0m")
        return self._execute_browser_action("click_element", {"index": index})

    @sisyphus_tool
    def browser_input_text(self,
                           index: Annotated[int, "The index of the element to input text into"],
                           text: Annotated[str, "The text to input"],
                           ) -> str:
        """Input text into an element

        Args:
            index (int): The index of the element to input text into
            text (str): The text to input

        Returns:
            dict: Result of the execution
        """
        logger.debug(f"Inputting text into element {index}: {text}\033[0m")
        return self._execute_browser_action("input_text", {"index": index, "text": text})

    @sisyphus_tool
    def browser_send_keys(self, keys: Annotated[
        str, "The keys to send (e.g., 'Enter', 'Escape', 'Control+a')"]) -> str:
        """Send keyboard keys

        Args:
            keys (str): The keys to send (e.g., 'Enter', 'Escape', 'Control+a')

        Returns:
            dict: Result of the execution
        """
        logger.debug(f"Sending keys: {keys}\033[0m")
        return self._execute_browser_action("send_keys", {"keys": keys})

    @sisyphus_tool
    def browser_switch_tab(self, page_id: Annotated[int, "The ID of the tab to switch to"]) -> str:
        """Switch to a different browser tab

        Args:
            page_id (int): The ID of the tab to switch to

        Returns:
            dict: Result of the execution
        """
        logger.debug(f"Switching to tab: {page_id}\033[0m")
        return self._execute_browser_action("switch_tab", {"page_id": page_id})

    @sisyphus_tool
    def browser_close_tab(self, page_id: Annotated[int, "The ID of the tab to close"]) -> str:
        """Close a browser tab

        Args:
            page_id (int): The ID of the tab to close

        Returns:
            dict: Result of the execution
        """
        logger.debug(f"Closing tab: {page_id}\033[0m")
        return self._execute_browser_action("close_tab", {"page_id": page_id})

    @sisyphus_tool
    def browser_scroll_down(self, amount: Annotated[
        int, "Pixel amount to scroll (if not specified, scrolls one page)"] = None) -> str:
        """Scroll down the page

        Args:
            amount (int, optional): Pixel amount to scroll. If None, scrolls one page.

        Returns:
            dict: Result of the execution
        """
        params = {}
        if amount is not None:
            params["amount"] = amount
            logger.debug(f"Scrolling down by {amount} pixels\033[0m")
        else:
            logger.debug(f"Scrolling down one page\033[0m")

        return self._execute_browser_action("scroll_down", params)

    @sisyphus_tool
    def browser_scroll_up(self, amount: Annotated[
        int, "Pixel amount to scroll (if not specified, scrolls one page)"] = None) -> str:
        """Scroll up the page

        Args:
            amount (int, optional): Pixel amount to scroll. If None, scrolls one page.

        Returns:
            dict: Result of the execution
        """
        params = {}
        if amount is not None:
            params["amount"] = amount
            logger.debug(f"Scrolling up by {amount} pixels\033[0m")
        else:
            logger.debug(f"Scrolling up one page\033[0m")

        return self._execute_browser_action("scroll_up", params)

    @sisyphus_tool
    def browser_scroll_to_text(self, text: Annotated[str, "The text to scroll to"]) -> str:
        """Scroll to specific text on the page

        Args:
            text (str): The text to scroll to

        Returns:
            dict: Result of the execution
        """
        logger.debug(f"Scrolling to text: {text}\033[0m")
        return self._execute_browser_action("scroll_to_text", {"text": text})

    @sisyphus_tool
    def browser_get_dropdown_options(self,
                                     index: Annotated[int, "The index of the dropdown element"]) -> str:
        """Get all options from a dropdown element

        Args:
            index (int): The index of the dropdown element

        Returns:
            dict: Result of the execution with the dropdown options
        """
        logger.debug(f"Getting options from dropdown with index: {index}\033[0m")
        return self._execute_browser_action("get_dropdown_options", {"index": index})

    @sisyphus_tool
    def browser_select_dropdown_option(self,
                                       index: Annotated[int, "The index of the dropdown element"],
                                       text: Annotated[str, "The text of the option to select"]) -> str:
        """Select an option from a dropdown by text

        Args:
            index (int): The index of the dropdown element
            text (str): The text of the option to select

        Returns:
            dict: Result of the execution
        """
        logger.debug(f"Selecting option '{text}' from dropdown with index: {index}\033[0m")
        return self._execute_browser_action("select_dropdown_option", {"index": index, "text": text})

    @sisyphus_tool
    def browser_drag_drop(self,
                          element_source: Annotated[str, "The source element selector"] = None,
                          element_target: Annotated[str, "The target element selector"] = None,
                          coord_source_x: Annotated[int, "The source X coordinate"] = None,
                          coord_source_y: Annotated[int, "The source Y coordinate"] = None,
                          coord_target_x: Annotated[int, "The target X coordinate"] = None,
                          coord_target_y: Annotated[int, "The target Y coordinate"] = None) -> str:
        """Perform drag and drop operation between elements or coordinates

        Args:
            element_source (str, optional): The source element selector
            element_target (str, optional): The target element selector
            coord_source_x (int, optional): The source X coordinate
            coord_source_y (int, optional): The source Y coordinate
            coord_target_x (int, optional): The target X coordinate
            coord_target_y (int, optional): The target Y coordinate

        Returns:
            dict: Result of the execution
        """
        params = {}

        if element_source and element_target:
            params["element_source"] = element_source
            params["element_target"] = element_target
            logger.debug(f"Dragging from element '{element_source}' to '{element_target}'\033[0m")
        elif all(coord is not None for coord in [coord_source_x, coord_source_y, coord_target_x, coord_target_y]):
            params["coord_source_x"] = coord_source_x
            params["coord_source_y"] = coord_source_y
            params["coord_target_x"] = coord_target_x
            params["coord_target_y"] = coord_target_y
            logger.debug(
                f"Dragging from coordinates ({coord_source_x}, {coord_source_y}) to ({coord_target_x}, {coord_target_y})\033[0m")
        else:
            return "Must provide either element selectors or coordinates for drag and drop"

        return self._execute_browser_action("drag_drop", params)

    @sisyphus_tool
    def browser_click_coordinates(self, x: Annotated[int, "The X coordinate to click"],
                                  y: Annotated[int, "The Y coordinate to click"]) -> str:
        """Click at specific X,Y coordinates on the page

        Args:
            x (int): The X coordinate to click
            y (int): The Y coordinate to click

        Returns:
            dict: Result of the execution
        """
        logger.debug(f"Clicking at coordinates: ({x}, {y})\033[0m")
        return self._execute_browser_action("click_coordinates", {"x": x, "y": y})

    @sisyphus_tool
    def get_browser_state(self) -> str:
        """Get the current state of the page

        Returns:
            dict: Result of the execution
        """
        logger.debug(f"Getting browser state\033[0m")
        return self._execute_browser_action("get_browser_state", method="GET")

    def _execute_browser_action(self, endpoint: str, params: dict = None, method: str = "POST") -> str:
        """Execute a browser automation action through the API

        Args:
            endpoint (str): The API endpoint to call
            params (dict, optional): Parameters to send. Defaults to None.
            method (str, optional): HTTP method to use. Defaults to "POST".

        Returns:
            str: Result of the execution
        """
        url = f"http://localhost:8000/api/automation/{endpoint}"

        headers = {
            'Content-Type': 'application/json'
        }

        if method == "GET" and params:
            response = requests.get(url, params=params, headers=headers, timeout=30)
        else:
            json_data = params if params else None
            response = requests.request(method, url, json=json_data, headers=headers, timeout=30)

        response.raise_for_status()
        logger.debug("Browser automation request completed successfully")

        return response.text
