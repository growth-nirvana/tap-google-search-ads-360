from singer_sdk import Tap, Stream
from singer_sdk import typing as th

from tap_search_ads.streams.customers import CustomersStream
from tap_search_ads.streams.campaigns import CampaignsStream
from tap_search_ads.streams.ad_groups import AdGroupsStream
from tap_search_ads.streams.ad_group_conversion_actions import AdGroupConversionActionsStream
from tap_search_ads.streams.ad_group_ads import AdGroupAdsStream
from tap_search_ads.streams.keywords import KeywordsStream
from tap_search_ads.streams.floodlight_activities import FloodlightActivitiesStream
from tap_search_ads.streams.pmax_conversions import PmaxConversionsStream
from tap_search_ads.streams.conversion_actions import ConversionActionsStream
from tap_search_ads.streams.campaign_conversions import CampaignConversionsStream
from tap_search_ads.streams.stream_floodlight_activities_new_api import FloodlightActivitiesNewApiStream
from tap_search_ads.streams.conversion_custom_variables import ConversionCustomVariablesStream
from tap_search_ads.streams.floodlight_activities_new_api_custom_dimension import FloodlightActivitiesNewApiCustomDimensionStream

class TapSearchAds(Tap):
    name = "tap-search-ads"

    config_jsonschema = th.PropertiesList(
        th.Property("client_id", th.StringType, required=True),
        th.Property("client_secret", th.StringType, required=True),
        th.Property("refresh_token", th.StringType, required=True),
        th.Property("login_customer_id", th.StringType, required=True),
        th.Property("customer_ids", th.StringType, required=True),  # comma-separated
        th.Property("start_date", th.StringType, required=False),
    ).to_dict()

    def discover_streams(self) -> list[Stream]:
        """Initialize all stream classes with parsed customer IDs from config."""
        raw_ids = self.config.get("customer_ids", "")
        customer_ids = [cid.strip() for cid in raw_ids.split(",") if cid.strip()]

        if not customer_ids:
            raise ValueError("No valid customer IDs provided in config['customer_ids'].")

        self.logger.info(f"Using {len(customer_ids)} customer IDs from config.")

        stream_classes = [
            AdGroupAdsStream,
            AdGroupsStream,
            AdGroupConversionActionsStream,
            CampaignsStream,
            CampaignConversionsStream,
            ConversionActionsStream,
            CustomersStream,
            FloodlightActivitiesStream,
            FloodlightActivitiesNewApiStream,
            KeywordsStream,
            PmaxConversionsStream,
            ConversionCustomVariablesStream,
            FloodlightActivitiesNewApiCustomDimensionStream,
        ]

        return [
            stream_class(self, customer_ids=customer_ids)
            for stream_class in stream_classes
        ]


cli = TapSearchAds.cli
