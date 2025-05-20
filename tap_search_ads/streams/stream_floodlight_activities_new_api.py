from singer_sdk import typing as th
from tap_search_ads.streams.base import SearchAdsStream

class FloodlightActivitiesNewApiStream(SearchAdsStream):
    name = "stream_floodlight_activities_new_api"
    primary_keys = ["ad_group.id", "segments.date"]
    replication_key = "segments.date"

    schema = th.PropertiesList(
        # Dimensions
        th.Property("ad_group.id", th.StringType),
        th.Property("ad_group.name", th.StringType),
        th.Property("campaign.id", th.StringType),
        th.Property("campaign.name", th.StringType),
        th.Property("customer.account_type", th.StringType),
        th.Property("customer.currency_code", th.StringType),
        th.Property("customer.descriptive_name", th.StringType),
        th.Property("customer.id", th.StringType),

        # Segments
        th.Property("segments.conversion_action_name", th.StringType),
        th.Property("segments.date", th.StringType),

        # Metrics
        th.Property("metrics.all_conversions", th.NumberType),
        th.Property("metrics.all_conversions_by_conversion_date", th.NumberType),
        th.Property("metrics.all_conversions_value", th.NumberType),
        th.Property("metrics.all_conversions_value_by_conversion_date", th.NumberType),
        th.Property("metrics.client_account_conversions", th.NumberType),
        th.Property("metrics.client_account_conversions_value", th.NumberType),
        th.Property("metrics.client_account_view_through_conversions", th.NumberType),
        th.Property("metrics.conversions", th.NumberType),
        th.Property("metrics.conversions_value", th.NumberType),
        th.Property("metrics.cross_device_conversions", th.NumberType),
        th.Property("metrics.cross_device_conversions_value", th.NumberType)
    ).to_dict()

    def get_query(self) -> str:
        return f"""
        SELECT
            -- Dimensions
            ad_group.id,
            ad_group.name,
            campaign.id,
            campaign.name,
            customer.account_type,
            customer.currency_code,
            customer.descriptive_name,
            customer.id,

            -- Segments
            segments.conversion_action_name,
            segments.date,

            -- Metrics
            metrics.all_conversions,
            metrics.all_conversions_by_conversion_date,
            metrics.all_conversions_value,
            metrics.all_conversions_value_by_conversion_date,
            metrics.client_account_conversions,
            metrics.client_account_conversions_value,
            metrics.client_account_view_through_conversions,
            metrics.conversions,
            metrics.conversions_value,
            metrics.cross_device_conversions,
            metrics.cross_device_conversions_value
        FROM ad_group
        {self.segments_date_filter()}
        """.strip() 