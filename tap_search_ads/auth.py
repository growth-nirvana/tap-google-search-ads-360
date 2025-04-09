import json
import requests
from typing import Optional, Dict

from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta
from singer_sdk.helpers._util import utc_now
from singer_sdk.streams import Stream as RESTStreamBase


def get_access_token_from_config(config: Dict) -> str:
    """Fetch a fresh access token from config values (tap or stream)."""
    token_resp = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": config["client_id"],
            "client_secret": config["client_secret"],
            "refresh_token": config["refresh_token"],
            "grant_type": "refresh_token"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token_resp.raise_for_status()
    return token_resp.json()["access_token"]


class ProxySearchAdsAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    def __init__(
        self,
        stream: RESTStreamBase,
        auth_endpoint: Optional[str] = None,
        oauth_scopes: Optional[str] = None,
        auth_headers: Optional[dict] = None,
        auth_body: Optional[dict] = None,
    ) -> None:
        super().__init__(stream=stream, auth_endpoint=auth_endpoint, oauth_scopes=oauth_scopes)
        self._auth_headers = auth_headers
        self._auth_body = auth_body

    def update_access_token(self) -> None:
        request_time = utc_now()
        token_response = requests.post(
            self.auth_endpoint,
            headers=self._auth_headers,
            data=json.dumps(self._auth_body)
        )
        token_response.raise_for_status()
        token_json = token_response.json()
        self.access_token = token_json["access_token"]
        self.expires_in = token_json["expires_in"]
        self.last_refreshed = request_time

    @property
    def oauth_request_body(self) -> dict:
        return {}


class SearchAdsAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    @property
    def oauth_request_body(self) -> dict:
        return {
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "refresh_token": self.config["refresh_token"],
            "grant_type": "refresh_token",
        }
