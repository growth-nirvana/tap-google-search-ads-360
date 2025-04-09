from singer_sdk import typing as th
from tap_search_ads.streams.base import SearchAdsStream

class PmaxConversionsStream(SearchAdsStream):
    name = "pmax_conversions"
    primary_keys = ["campaign.id", "segments.date", "segments.conversion_action_name"]
    replication_key = None

    schema = th.PropertiesList(
        # Attributes
        th.Property("campaign.id", th.StringType),
        th.Property("campaign.name", th.StringType),
        th.Property("campaign.advertising_channel_type", th.StringType),
        th.Property("campaign.selective_optimization.conversion_actions", th.ArrayType(th.StringType)),
        th.Property("campaign.resource_name", th.StringType),
        th.Property("customer.id", th.StringType),
        th.Property("customer.descriptive_name", th.StringType),
        th.Property("customer.resource_name", th.StringType),

        # Metrics
        th.Property("metrics.all_conversions", th.NumberType),
        th.Property("metrics.all_conversions_value", th.NumberType),
        th.Property("metrics.conversions", th.NumberType),

        # Segments
        th.Property("segments.date", th.StringType),
        th.Property("segments.conversion_action_name", th.StringType),
        th.Property("segments.conversion_action", th.StringType)
    ).to_dict()

    def get_query(self) -> str:
        return f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.advertising_channel_type,
            campaign.selective_optimization.conversion_actions,
            campaign.resource_name,
            customer.id,
            customer.descriptive_name,
            customer.resource_name,
            metrics.all_conversions,
            metrics.all_conversions_value,
            metrics.conversions,
            segments.date,
            segments.conversion_action_name,
            segments.conversion_action
        FROM campaign
        {self.segments_date_filter()}
        """.strip()
