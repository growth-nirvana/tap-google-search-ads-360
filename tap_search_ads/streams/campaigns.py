from singer_sdk import typing as th
from tap_search_ads.streams.base import SearchAdsStream

class CampaignsStream(SearchAdsStream):
    name = "campaigns"
    primary_keys = ["campaign.id", "segments.date"]
    replication_key = None

    schema = th.PropertiesList(
        # Attributes
        th.Property("campaign.id", th.StringType),
        th.Property("campaign.name", th.StringType),
        th.Property("campaign.status", th.StringType),
        th.Property("campaign.resource_name", th.StringType),
        th.Property("campaign.engine_id", th.StringType),
        th.Property("campaign.advertising_channel_type", th.StringType),
        th.Property("campaign.bidding_strategy", th.StringType),
        th.Property("campaign.campaign_budget", th.StringType),
        th.Property("campaign.start_date", th.StringType),
        th.Property("campaign.end_date", th.StringType),
        th.Property("campaign.labels", th.ArrayType(th.StringType)),

        # Metrics
        th.Property("metrics.clicks", th.NumberType),
        th.Property("metrics.cost_micros", th.NumberType),
        th.Property("metrics.impressions", th.NumberType),
        th.Property("metrics.conversions", th.NumberType),
        th.Property("metrics.all_conversions", th.NumberType),
        th.Property("metrics.all_conversions_value", th.NumberType),
        th.Property("metrics.client_account_conversions", th.NumberType),

        # Segments
        th.Property("segments.date", th.StringType),
    ).to_dict()

    def get_query(self) -> str:
        return f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.resource_name,
            campaign.engine_id,
            campaign.advertising_channel_type,
            campaign.bidding_strategy,
            campaign.campaign_budget,
            campaign.start_date,
            campaign.end_date,
            campaign.labels,
            metrics.clicks,
            metrics.cost_micros,
            metrics.impressions,
            metrics.conversions,
            metrics.all_conversions,
            metrics.all_conversions_value,
            metrics.client_account_conversions,
            segments.date
        FROM campaign
        {self.segments_date_filter()}
        """.strip()
