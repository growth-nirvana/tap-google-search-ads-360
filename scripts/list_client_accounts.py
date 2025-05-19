#!/usr/bin/env python3

import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from dotenv import load_dotenv
import os
from pathlib import Path

def get_access_token(client_id, client_secret, refresh_token):
    creds = Credentials(
        None,  # token is None to force refresh
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri="https://oauth2.googleapis.com/token",
        scopes=['https://www.googleapis.com/auth/doubleclicksearch']  # Add required scope
    )
    creds.refresh(Request())
    return creds.token

def main():
    # Force reload environment variables from .env file
    script_dir = Path(__file__).parent
    env_path = script_dir / '.env'
    load_dotenv(dotenv_path=env_path, override=True)  # Add override=True to force reload
    
    # Get credentials from environment variables
    client_id = os.environ['GOOGLE_CLIENT_ID']  # Use os.environ instead of os.getenv
    client_secret = os.environ['GOOGLE_CLIENT_SECRET']
    refresh_token = os.environ['GOOGLE_REFRESH_TOKEN']
    
    if not all([client_id, client_secret, refresh_token]):
        print("Error: Missing required environment variables. Please set:")
        print("GOOGLE_CLIENT_ID - Your OAuth client ID")
        print("GOOGLE_CLIENT_SECRET - Your OAuth client secret")
        print("GOOGLE_REFRESH_TOKEN - Your OAuth refresh token")
        print(f"\nMake sure these are set in: {env_path}")
        return
    
    # Get access token
    access_token = get_access_token(client_id, client_secret, refresh_token)
    
    # First, get all accessible customers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(
        "https://searchads360.googleapis.com/v0/customers:listAccessibleCustomers",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        if 'resourceNames' in data:
            print("\nAccessible Customers:")
            print("-" * 50)
            
            for resource_name in data['resourceNames']:
                customer_id = resource_name.split('/')[-1]
                
                # For each customer, get their client accounts
                query = """
                SELECT
                    customer_client.descriptive_name,
                    customer_client.client_customer,
                    customer_client.status
                FROM customer_client
                """
                
                client_response = requests.post(
                    f"https://searchads360.googleapis.com/v0/customers/{customer_id}/searchAds360:search",
                    headers=headers,
                    json={"query": query}
                )
                
                if client_response.status_code == 200:
                    client_data = client_response.json()
                    if 'results' in client_data:
                        print(f"\nCustomer ID: {customer_id}")
                        print(f"Resource Name: {resource_name}")
                        print("Client Accounts:")
                        print("-" * 30)
                        
                        for result in client_data['results']:
                            client = result.get('customerClient', {})
                            print(f"Name: {client.get('descriptiveName', 'N/A')}")
                            print(f"Client ID: {client.get('clientCustomer', 'N/A')}")
                            print(f"Status: {client.get('status', 'N/A')}")
                            print("-" * 30)
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main() 