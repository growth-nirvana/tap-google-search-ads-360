from singer_sdk import typing as th
from tap_search_ads.streams.base import SearchAdsStream

class CampaignsStream(SearchAdsStream):
    name = "campaigns"
    primary_keys = ["campaign.id"]
    replication_key = None

    schema = th.PropertiesList(
        th.Property("campaign.id", th.StringType),
        th.Property("campaign.name", th.StringType),
        th.Property("campaign.status", th.StringType),
        th.Property("campaign.resource_name", th.StringType),
    ).to_dict()

    def get_query(self) -> str:
        start_date = self.config.get("start_date")
        end_date = self.config.get("end_date")
        date_filter = ""
        if start_date and end_date:
            date_filter = f"WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'"
        return f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.resource_name
        FROM campaign
        {date_filter}
        """.strip()
