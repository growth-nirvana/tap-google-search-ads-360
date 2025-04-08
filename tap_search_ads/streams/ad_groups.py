from singer_sdk import typing as th
from tap_search_ads.streams.base import SearchAdsStream

class AdGroupsStream(SearchAdsStream):
    name = "ad_groups"
    primary_keys = ["ad_group.id"]
    replication_key = None

    schema = th.PropertiesList(
        # Attributes
        th.Property("ad_group.id", th.StringType),
        th.Property("ad_group.name", th.StringType),
        th.Property("ad_group.status", th.StringType),
        th.Property("ad_group.resource_name", th.StringType),
        th.Property("ad_group.engine_id", th.StringType),
        th.Property("ad_group.engine_status", th.StringType),
        th.Property("accessible_bidding_strategy.name", th.StringType),
        th.Property("accessible_bidding_strategy.owner_customer_id", th.StringType),

        # Metrics (confirmed compatible)
        th.Property("metrics.cost_micros", th.NumberType),
        th.Property("metrics.impressions", th.NumberType),
        th.Property("metrics.visits", th.NumberType),
        th.Property("metrics.average_cpm", th.NumberType),

        # Segments (safe)
        th.Property("segments.date", th.StringType)
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
            ad_group.status,
            ad_group.resource_name,
            ad_group.engine_id,
            ad_group.engine_status,
            accessible_bidding_strategy.name,
            accessible_bidding_strategy.owner_customer_id,
            metrics.cost_micros,
            metrics.impressions,
            metrics.visits,
            metrics.average_cpm,
            segments.date
        FROM ad_group
        {date_filter}
        """.strip()
