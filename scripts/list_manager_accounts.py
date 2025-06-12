#!/usr/bin/env python3

import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from dotenv import load_dotenv
import os

def get_access_token(client_id, client_secret, refresh_token):
    creds = Credentials(
        None,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri="https://oauth2.googleapis.com/token"
    )
    creds.refresh(Request())
    return creds.token

def get_customer_details(access_token, customer_id, login_customer_id=None):
    """Get details about a specific customer."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    if login_customer_id:
        headers["login-customer-id"] = login_customer_id
    
    query = """
    SELECT
        customer.id,
        customer.descriptive_name,
        customer.manager,
        customer.account_type
    FROM customer
    """
    
    response = requests.post(
        f"https://searchads360.googleapis.com/v0/customers/{customer_id}/searchAds360:search",
        headers=headers,
        json={"query": query}
    )
    
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            return data['results'][0].get('customer', {})
    return None

def get_managed_accounts(access_token, manager_id):
    """Get all accounts managed by a manager account."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "login-customer-id": manager_id
    }
    
    query = """
    SELECT
        customer.id,
        customer.descriptive_name,
        customer.manager,
        customer.account_type
    FROM customer
    """
    
    response = requests.post(
        f"https://searchads360.googleapis.com/v0/customers/{manager_id}/searchAds360:search",
        headers=headers,
        json={"query": query}
    )
    
    if response.status_code == 200:
        data = response.json()
        if 'results' in data:
            return data['results']
    return []

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get credentials from environment variables
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    refresh_token = os.getenv('GOOGLE_REFRESH_TOKEN')
    
    if not all([client_id, client_secret, refresh_token]):
        print("Error: Missing required environment variables. Please set:")
        print("GOOGLE_CLIENT_ID - Your OAuth client ID")
        print("GOOGLE_CLIENT_SECRET - Your OAuth client secret")
        print("GOOGLE_REFRESH_TOKEN - Your OAuth refresh token")
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
            
            # First pass: identify manager accounts
            manager_accounts = []
            for resource_name in data['resourceNames']:
                customer_id = resource_name.split('/')[-1]
                customer = get_customer_details(access_token, customer_id)
                
                if customer:
                    print(f"Customer ID: {customer_id}")
                    print(f"Name: {customer.get('descriptiveName', 'N/A')}")
                    print(f"Account Type: {customer.get('accountType', 'N/A')}")
                    print(f"Is Manager: {customer.get('manager', False)}")
                    print(f"Resource Name: {resource_name}")
                    print("-" * 50)
                    
                    # If this is a manager account, add it to our list
                    if customer.get('manager', False):
                        manager_accounts.append(customer_id)
            
            # Second pass: for each manager account, list all managed accounts
            if manager_accounts:
                print("\nManaged Accounts:")
                print("-" * 50)
                for manager_id in manager_accounts:
                    manager = get_customer_details(access_token, manager_id)
                    if manager:
                        print(f"\nManager Account: {manager.get('descriptiveName', 'N/A')} (ID: {manager_id})")
                        print("Managed Accounts:")
                        print("-" * 30)
                        
                        managed_accounts = get_managed_accounts(access_token, manager_id)
                        for account in managed_accounts:
                            customer = account.get('customer', {})
                            print(f"Customer ID: {customer.get('id', 'N/A')}")
                            print(f"Name: {customer.get('descriptiveName', 'N/A')}")
                            print(f"Account Type: {customer.get('accountType', 'N/A')}")
                            print(f"Is Manager: {customer.get('manager', False)}")
                            print("-" * 30)
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main() 