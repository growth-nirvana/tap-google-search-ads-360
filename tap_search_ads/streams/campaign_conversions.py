from singer_sdk import typing as th
from tap_search_ads.streams.base import SearchAdsStream

class CampaignConversionsStream(SearchAdsStream):
    name = "campaign_conversions"
    primary_keys = ["campaign.id", "segments.date", "segments.conversion_action_name"]
    replication_key = None

    schema = th.PropertiesList(
        th.Property("campaign.id", th.StringType),
        th.Property("campaign.resource_name", th.StringType),
        th.Property("segments.date", th.StringType),
        th.Property("segments.conversion_action", th.StringType),
        th.Property("segments.conversion_action_name", th.StringType),
        th.Property("segments.conversion_action_category", th.StringType),
        th.Property("segments.ad_network_type", th.StringType),
    ).to_dict()

    def get_query(self) -> str:
        return f"""
        SELECT
            campaign.id,
            campaign.resource_name,
            segments.date,
            segments.conversion_action,
            segments.conversion_action_name,
            segments.conversion_action_category,
            segments.ad_network_type
        FROM campaign
        {self.segments_date_filter()}
        """.strip()
