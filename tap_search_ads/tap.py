from singer_sdk import Tap, Stream
from singer_sdk import typing as th

from tap_search_ads.streams.customers import CustomersStream
from tap_search_ads.streams.campaigns import CampaignsStream
from tap_search_ads.streams.ad_groups import AdGroupsStream

class TapSearchAds(Tap):
    name = "tap-search-ads"

    config_jsonschema = th.PropertiesList(
        th.Property("client_id", th.StringType, required=True),
        th.Property("client_secret", th.StringType, required=True),
        th.Property("refresh_token", th.StringType, required=True),
        th.Property("customer_ids", th.ArrayType(th.StringType), required=True),
        th.Property("start_date", th.StringType, required=False),
        th.Property("end_date", th.StringType, required=False)
    ).to_dict()

    def discover_streams(self) -> list[Stream]:
        return [
            CustomersStream(self),
            CampaignsStream(self),
            AdGroupsStream(self)
        ]

cli = TapSearchAds.cli