from typing import Any
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import logging
import json
import time

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
        url = f"https://searchads360.googleapis.com/v0/customers/{customer_id}/searchAds360:search"
        headers = {
            "Authorization": f"Bearer {get_access_token(self.config)}",
            "Content-Type": "application/json"
        }
        login_customer_id = self.config.get("login_customer_id")
        if login_customer_id:
            headers["login-customer-id"] = login_customer_id
        data = {"query": query}
        all_results = []
        next_page_token = None
        while True:
            if next_page_token:
                data["page_token"] = next_page_token
            response = requests.post(url, headers=headers, json=data)
            if response.status_code != 200:
                error_data = response.json()
                error_details = error_data.get('error', {}).get('details', [])
                for detail in error_details:
                    if detail.get('errorCode', {}).get('quotaError') == 'RESOURCE_EXHAUSTED':
                        logger.warning("Quota exhausted. Waiting 960 seconds before retrying...")
                        time.sleep(960)
                        continue  # Retry the request
                error_msg = f"API request failed with status {response.status_code}"
                try:
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
            response_data = response.json()
            results = response_data.get('results', [])
            all_results.extend(results)
            next_page_token = response_data.get('next_page_token')
            if not next_page_token:
                break
        return {"results": all_results}
