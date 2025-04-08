from singer_sdk import typing as th
from tap_search_ads.streams.base import SearchAdsStream

class AdGroupAdsStream(SearchAdsStream):
    name = "ad_group_ads"
    primary_keys = ["ad_group_ad.ad.id", "segments.date"]
    replication_key = None

    schema = th.PropertiesList(
        # Attributes
        th.Property("ad_group_ad.ad.id", th.StringType),
        th.Property("ad_group_ad.ad.name", th.StringType),
        th.Property("ad_group_ad.ad.type", th.StringType),
        th.Property("ad_group_ad.ad.resource_name", th.StringType),
        th.Property("ad_group_ad.status", th.StringType),
        th.Property("ad_group_ad.resource_name", th.StringType),
        th.Property("ad_group.id", th.StringType),
        th.Property("ad_group.name", th.StringType),
        th.Property("ad_group.engine_status", th.StringType),
        th.Property("ad_group.resource_name", th.StringType),

        # Metrics
        th.Property("metrics.clicks", th.NumberType),
        th.Property("metrics.cost_micros", th.NumberType),
        th.Property("metrics.impressions", th.NumberType),
        th.Property("metrics.average_cpc", th.NumberType),
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
            ad_group_ad.ad.id,
            ad_group_ad.ad.name,
            ad_group_ad.ad.type,
            ad_group_ad.ad.resource_name,
            ad_group_ad.status,
            ad_group_ad.resource_name,
            ad_group.id,
            ad_group.name,
            ad_group.engine_status,
            ad_group.resource_name,
            metrics.clicks,
            metrics.cost_micros,
            metrics.impressions,
            metrics.average_cpc,
            metrics.all_conversions,
            metrics.all_conversions_value,
            segments.date
        FROM ad_group_ad
        {date_filter}
        """.strip()
