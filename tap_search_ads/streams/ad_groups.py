from singer_sdk import typing as th
from tap_search_ads.streams.base import SearchAdsStream

class AdGroupsStream(SearchAdsStream):
    name = "ad_groups"
    primary_keys = ["ad_group.id"]
    replication_key = None

    schema = th.PropertiesList(
        th.Property("ad_group.id", th.StringType),
        th.Property("ad_group.name", th.StringType),
        th.Property("ad_group.status", th.StringType),
        th.Property("ad_group.resource_name", th.StringType),
    ).to_dict()

    def get_query(self) -> str:
        start_date = self.config.get("start_date")
        end_date = self.config.get("end_date")
        date_filter = ""
        if start_date and end_date:
            date_filter = f"WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'"
        return f"""
        SELECT
            ad_group.id,
            ad_group.name,
            ad_group.status,
            ad_group.resource_name
        FROM ad_group
        {date_filter}
        """.strip()
