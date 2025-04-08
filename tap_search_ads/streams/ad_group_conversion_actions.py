from singer_sdk import typing as th
from tap_search_ads.streams.base import SearchAdsStream

class AdGroupConversionActionsStream(SearchAdsStream):
    name = "ad_group_conversion_actions"
    primary_keys = ["ad_group.id", "segments.date", "segments.conversion_action_name"]
    replication_key = None

    schema = th.PropertiesList(
        # Attributes
        th.Property("ad_group.id", th.StringType),
        th.Property("ad_group.name", th.StringType),
        th.Property("ad_group.resource_name", th.StringType),
        th.Property("campaign.id", th.StringType),
        th.Property("campaign.resource_name", th.StringType),

        # Metrics
        th.Property("metrics.conversions", th.NumberType),
        th.Property("metrics.all_conversions", th.NumberType),
        th.Property("metrics.all_conversions_value", th.NumberType),
        th.Property("metrics.client_account_conversions", th.NumberType),

        # Segments
        th.Property("segments.date", th.StringType),
        th.Property("segments.conversion_action_name", th.StringType)
    ).to_dict()

    def get_query(self) -> str:
        start_date, end_date = self.get_date_range()
        date_filter = ""
        if start_date and end_date:
            date_filter = f"WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'"

        return f"""
        SELECT
            ad_group.id,
            ad_group.name,
            ad_group.resource_name,
            campaign.id,
            campaign.resource_name,
            metrics.conversions,
            metrics.all_conversions,
            metrics.all_conversions_value,
            metrics.client_account_conversions,
            segments.date,
            segments.conversion_action_name
        FROM ad_group
        {date_filter}
        """.strip()
