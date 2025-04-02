
from typing import Dict
from singer_sdk import typing as th
from tap_search_ads.streams.base import SearchAdsStream


class CustomersStream(SearchAdsStream):
    name = "customers"
    path = "/customers:search"
    primary_keys = ["customer.id"]

    schema = th.PropertiesList(
        th.Property("customer.id", th.StringType),
        th.Property("customer.resource_name", th.StringType),
        th.Property("customer.descriptive_name", th.StringType),
        th.Property("customer.status", th.StringType),
        th.Property("customer.manager", th.StringType),
    ).to_dict()

    def get_query(self) -> str:
        return """
        SELECT
          customer.id,
          customer.resource_name,
          customer.descriptive_name,
          customer.status,
          customer.manager
        FROM customer
        """.strip()