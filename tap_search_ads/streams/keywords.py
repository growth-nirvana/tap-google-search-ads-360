from singer_sdk import typing as th
from tap_search_ads.streams.base import SearchAdsStream

class KeywordsStream(SearchAdsStream):
    name = "keywords"
    primary_keys = ["ad_group_criterion.criterion_id", "segments.date"]
    replication_key = None

    schema = th.PropertiesList(
        # Attributes
        th.Property("ad_group_criterion.criterion_id", th.StringType),
        th.Property("ad_group_criterion.keyword.text", th.StringType),
        th.Property("ad_group_criterion.keyword.match_type", th.StringType),
        th.Property("ad_group_criterion.status", th.StringType),
        th.Property("ad_group_criterion.resource_name", th.StringType),
        th.Property("ad_group.id", th.StringType),
        th.Property("ad_group.resource_name", th.StringType),
        th.Property("campaign.id", th.StringType),
        th.Property("campaign.resource_name", th.StringType),
        th.Property("keyword_view.resource_name", th.StringType),

        # Metrics
        th.Property("metrics.impressions", th.NumberType),
        th.Property("metrics.clicks", th.NumberType),
        th.Property("metrics.cost_micros", th.NumberType),
        th.Property("metrics.conversions", th.NumberType),
        th.Property("metrics.all_conversions", th.NumberType),
        th.Property("metrics.all_conversions_value", th.NumberType),

        # Segments
        th.Property("segments.date", th.StringType)
    ).to_dict()

    def get_query(self) -> str:
        start_date = self.config.get("start_date")
        end_date = self.config.get("end_date")
        date_filter = ""
        if start_date and end_date:
            date_filter = f"WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'"

        return f"""
        SELECT
            ad_group_criterion.criterion_id,
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            ad_group_criterion.status,
            ad_group_criterion.resource_name,
            ad_group.id,
            ad_group.resource_name,
            campaign.id,
            campaign.resource_name,
            keyword_view.resource_name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.all_conversions,
            metrics.all_conversions_value,
            segments.date
        FROM keyword_view
        {date_filter}
        """.strip()
