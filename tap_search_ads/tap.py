from singer_sdk import Tap, Stream
from singer_sdk import typing as th
import requests

from tap_search_ads.auth import get_access_token_from_config

from tap_search_ads.streams.customers import CustomersStream
from tap_search_ads.streams.campaigns import CampaignsStream
from tap_search_ads.streams.ad_groups import AdGroupsStream
from tap_search_ads.streams.ad_group_conversion_actions import AdGroupConversionActionsStream
from tap_search_ads.streams.ad_group_ads import AdGroupAdsStream
from tap_search_ads.streams.keywords import KeywordsStream
from tap_search_ads.streams.floodlight_activities import FloodlightActivitiesStream
from tap_search_ads.streams.pmax_conversions import PmaxConversionsStream
from tap_search_ads.streams.conversion_actions import ConversionActionsStream


class TapSearchAds(Tap):
    name = "tap-search-ads"

    config_jsonschema = th.PropertiesList(
        th.Property("client_id", th.StringType, required=True),
        th.Property("client_secret", th.StringType, required=True),
        th.Property("refresh_token", th.StringType, required=True),
        th.Property("login_customer_id", th.StringType, required=True),  # Required for manager context
        th.Property("start_date", th.StringType, required=False),
    ).to_dict()

    def get_all_customer_ids_recursive(self) -> list[str]:
        """Recursively retrieve all advertiser customer IDs from the login MCC."""
        access_token = get_access_token_from_config(self.config)
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "login-customer-id": self.config["login_customer_id"]
        }

        visited = set()
        advertiser_ids = []

        def fetch_children(parent_id: str):
            if parent_id in visited:
                return
            visited.add(parent_id)

            body = {
                "query": (
                    "SELECT customer_client.client_customer, "
                    "customer_client.manager "
                    "FROM customer_client"
                )
            }

            resp = requests.post(
                f"https://searchads360.googleapis.com/v0/customers/{parent_id}/searchAds360:search",
                headers=headers,
                json=body
            )

            if resp.status_code == 404:
                self.logger.warning(f"Customer {parent_id} not found or inaccessible.")
                return

            resp.raise_for_status()
            results = resp.json().get("results", [])

            for row in results:
                customer = row.get("customerClient", {})
                resource = customer.get("clientCustomer")
                if not resource:
                    continue

                customer_id = resource.split("/")[1]

                if customer.get("manager", False):
                    fetch_children(customer_id)  # Recurse into sub-MCC
                else:
                    advertiser_ids.append(customer_id)

        # Start recursion from the login customer
        fetch_children(self.config["login_customer_id"])

        self.logger.info(f"Discovered {len(advertiser_ids)} advertiser customer IDs.")
        return advertiser_ids

    def discover_streams(self) -> list[Stream]:
        """Dynamically discover all streams and inject discovered customer IDs."""
        customer_ids = self.get_all_customer_ids_recursive()

        stream_classes = [
            AdGroupAdsStream,
            AdGroupsStream,
            AdGroupConversionActionsStream,
            CampaignsStream,
            ConversionActionsStream,
            CustomersStream,
            FloodlightActivitiesStream,
            KeywordsStream,
            PmaxConversionsStream,
        ]

        return [
            stream_class(self, customer_ids=customer_ids)
            for stream_class in stream_classes
        ]


cli = TapSearchAds.cli
