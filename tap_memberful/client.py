"""GraphQL client handling, including MemberfulStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.streams import GraphQLStream


class MemberfulStream(GraphQLStream):
    """Memberful stream class."""

    url_base = "https://vox.memberful.com/api/graphql"

    @property
    def next_page_token_jsonpath(self):
        return f"$.data.{self.name}.pageInfo.endCursor"

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        return BearerTokenAuthenticator(
            stream=self,
            token=self.config.get("api_key")
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        # Pass empty string instead of `None` to avoid error on first page
        return {"afterCursor": next_page_token or ""}

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        resp_json = response.json()
        try:
            # TODO: Generalize - get_records() method that streams can override?
            if self.name == "plans":
                for row in resp_json.get("data", {}).get(self.name, {}):
                    yield row
            else:
                for row in resp_json.get("data", {}).get(self.name, {}).get("edges"):
                    yield row.get("node", {})

        except TypeError as e:
            # TODO: Add explicit error handling when response has errors array
            print("Damn this is gonna fail")
            print(self.query)
            print(resp_json)
            raise e

    # def get_next_page_token(
    #     self, response: requests.Response, previous_token: Optional[Any]
    # ) -> Any:
    #     pass

    # def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
    #     """As needed, append or transform raw data to match expected structure."""
    #     # TODO: Delete this method if not needed.
    #     return row
