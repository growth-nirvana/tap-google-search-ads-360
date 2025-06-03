from singer_sdk import typing as th
from tap_search_ads.streams.base import SearchAdsStream

class ConversionCustomVariablesStream(SearchAdsStream):
    name = "conversion_custom_variables"
    primary_keys = ["customer.id", "conversion_custom_variable.id"]
    replication_key = None

    schema = th.PropertiesList(
        th.Property("customer.id", th.StringType),
        th.Property("conversion_custom_variable.id", th.StringType),
        th.Property("conversion_custom_variable.name", th.StringType),
        th.Property("conversion_custom_variable.tag", th.StringType),
        th.Property("conversion_custom_variable.floodlight_conversion_custom_variable_info.floodlight_variable_type", th.StringType),
    ).to_dict()

    def get_query(self) -> str:
        return """
        SELECT 
            customer.id,
            conversion_custom_variable.id,
            conversion_custom_variable.name,
            conversion_custom_variable.tag,
            conversion_custom_variable.floodlight_conversion_custom_variable_info.floodlight_variable_type
        FROM conversion_custom_variable
        """.strip()
