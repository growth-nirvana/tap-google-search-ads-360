
from typing import Any
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


def get_access_token(config):
    creds = Credentials(
        None,
        refresh_token=config["refresh_token"],
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        token_uri="https://oauth2.googleapis.com/token"
    )
    creds.refresh(Request())
    return creds.token


class SA360Client:
    def __init__(self, stream):
        self.stream = stream
        self.config = stream.config

    def generate_report(self, query: str, customer_id: str) -> dict:
        headers = {
            "Authorization": f"Bearer {get_access_token(self.config)}",
            "Content-Type": "application/json"
        }

        login_customer_id = self.config.get("login_customer_id")
        if login_customer_id:
            headers["login-customer-id"] = login_customer_id

        url = f"https://searchads360.googleapis.com/v0/customers/{customer_id}/searchAds360:search"

        response = requests.post(
            url,
            headers=headers,
            json={"query": query, "pageSize": 1000}
        )
        response.raise_for_status()
        return response.json()
