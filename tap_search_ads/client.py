from typing import Any
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import logging
import json

logger = logging.getLogger(__name__)

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
        
        # Debug logging
        logger.info(f"Making request to: {url}")
        logger.info(f"Headers: {headers}")
        logger.info(f"Query: {query}")

        response = requests.post(
            url,
            headers=headers,
            json={"query": query, "pageSize": 1000}
        )
        
        # Debug logging
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response body: {response.text}")
        
        if response.status_code != 200:
            error_msg = f"API request failed with status {response.status_code}"
            try:
                error_data = response.json()
                if 'error' in error_data:
                    error_details = error_data['error']
                    error_msg = f"API Error: {error_details.get('message', 'Unknown error')}"
                    if 'details' in error_details:
                        for detail in error_details['details']:
                            if 'errors' in detail:
                                for err in detail['errors']:
                                    error_msg += f"\nError Code: {err.get('errorCode', {}).get('queryError', 'Unknown')}"
                                    error_msg += f"\nError Message: {err.get('message', 'No message')}"
            except json.JSONDecodeError:
                error_msg += f"\nResponse text: {response.text}"
            
            logger.error(error_msg)
            raise requests.exceptions.HTTPError(error_msg, response=response)
            
        return response.json()
