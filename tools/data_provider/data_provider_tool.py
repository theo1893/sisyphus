import json
from typing import Union, Dict, Any, Annotated

from tools.data_provider.linkedin import LinkedinProvider
from tools.data_provider.twitter import TwitterProvider
from tools.util import sisyphus_tool, sisyphus_register


class DataProvidersTool:
    def __init__(self):
        self.register_data_providers = {
            "linkedin": LinkedinProvider(),
            "twitter": TwitterProvider(),
        }
        sisyphus_register(self)

    @sisyphus_tool
    def get_data_provider_endpoints(
            self,
            service_name: Annotated[
                str, "The name of the data provider (e.g., 'linkedin', 'twitter', 'zillow', 'amazon', 'yahoo_finance'"]
    ):
        """
        Get available endpoints for a specific data provider.
        """

        try:
            if not service_name:
                return "Data provider name is required."

            if service_name not in self.register_data_providers:
                return f"Data provider '{service_name}' not found. Available data providers: {list(self.register_data_providers.keys())}"

            endpoints = self.register_data_providers[service_name].get_endpoints()
            return endpoints

        except Exception as e:
            error_message = str(e)
            simplified_message = f"Error getting data provider endpoints: {error_message[:200]}"
            if len(error_message) > 200:
                simplified_message += "..."
            return simplified_message

    @sisyphus_tool
    def execute_data_provider_call(
            self,
            service_name: Annotated[
                str, "The name of the data provider (e.g., 'linkedin', 'twitter', 'zillow', 'amazon', 'yahoo_finance'"],
            endpoint: Annotated[str, "The endpoint to call"],
            payload: Annotated[Union[Dict[
                str, Any], str, None], "The payload to send with the data provider call (dict or JSON string)"] = None
    ):
        """Execute a call to a specific data provider endpoint."""

        try:
            if isinstance(payload, str):
                try:
                    payload = json.loads(payload)
                except json.JSONDecodeError as e:
                    return f"Invalid JSON in payload: {str(e)}"
            elif payload is None:
                payload = {}

            if not service_name:
                return "service_name is required."

            if not endpoint:
                return "endpoint is required."

            if service_name not in self.register_data_providers:
                return f"API '{service_name}' not found. Available APIs: {list(self.register_data_providers.keys())}"

            data_provider = self.register_data_providers[service_name]

            if endpoint not in data_provider.get_endpoints().keys():
                return f"Endpoint '{endpoint}' not found in {service_name} data provider."

            result = data_provider.call_endpoint(endpoint, payload)
            return result

        except Exception as e:
            error_message = str(e)
            simplified_message = f"Error executing data provider call: {error_message[:200]}"
            if len(error_message) > 200:
                simplified_message += "..."
            return simplified_message
