from singer_sdk import typing as th
from tap_search_ads.streams.base import SearchAdsStream


class CustomersStream(SearchAdsStream):
    name = "customers"
    primary_keys = ["customer.id"]
    replication_key = None

    schema = th.PropertiesList(
        th.Property("customer.id", th.StringType),
        th.Property("customer.resource_name", th.StringType),
        th.Property("customer.descriptive_name", th.StringType),
        th.Property("customer.status", th.StringType),
        th.Property("customer.manager", th.StringType),
        th.Property("customer.account_status", th.StringType),
        th.Property("customer.account_type", th.StringType),
        th.Property("customer.currency_code", th.StringType),
        th.Property("customer.engine_id", th.StringType),
    ).to_dict()

    def get_query(self, **kwargs) -> str:
        return """
        SELECT
          customer.id,
          customer.resource_name,
          customer.descriptive_name,
          customer.status,
          customer.manager,
          customer.account_status,
          customer.account_type,
          customer.currency_code,
          customer.engine_id
        FROM customer
        """.strip()
