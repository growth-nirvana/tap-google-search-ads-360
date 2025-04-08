from singer_sdk import typing as th
from tap_search_ads.streams.base import SearchAdsStream

class ConversionActionsStream(SearchAdsStream):
    name = "conversion_actions"
    primary_keys = ["conversion_action.id"]
    replication_key = None

    schema = th.PropertiesList(
        th.Property("conversion_action.id", th.StringType),
        th.Property("conversion_action.name", th.StringType),
        th.Property("conversion_action.category", th.StringType),
        th.Property("conversion_action.type", th.StringType),
        th.Property("conversion_action.status", th.StringType),
        th.Property("conversion_action.creation_time", th.StringType),
        th.Property("conversion_action.resource_name", th.StringType),
        th.Property("conversion_action.floodlight_settings.activity_group_tag", th.StringType),
    ).to_dict()

    def get_query(self) -> str:
        return """
        SELECT
            conversion_action.id,
            conversion_action.name,
            conversion_action.category,
            conversion_action.type,
            conversion_action.status,
            conversion_action.creation_time,
            conversion_action.resource_name,
            conversion_action.floodlight_settings.activity_group_tag
        FROM conversion_action
        """.strip()
