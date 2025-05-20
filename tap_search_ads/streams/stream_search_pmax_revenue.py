from singer_sdk import typing as th
from tap_search_ads.streams.base import SearchAdsStream

class StreamSearchPmaxRevenue(SearchAdsStream):
    name = "stream_search_pmax_revenue"
    primary_keys = ["campaign.id", "segments.date"]
    replication_key = None

    schema = th.PropertiesList(
        # Campaign Attributes
        th.Property("campaign.bidding_strategy", th.StringType),
        th.Property("campaign.campaign_budget", th.StringType),
        th.Property("campaign.end_date", th.StringType),
        th.Property("campaign.engine_id", th.StringType),
        th.Property("campaign.id", th.StringType),
        th.Property("campaign.labels", th.ArrayType(th.StringType)),
        th.Property("campaign.last_modified_time", th.StringType),
        th.Property("campaign.name", th.StringType),
        th.Property("campaign.resource_name", th.StringType),
        th.Property("campaign.start_date", th.StringType),
        th.Property("campaign.status", th.StringType),

        # Campaign Budget
        th.Property("campaign_budget.amount_micros", th.NumberType),

        # Customer Attributes
        th.Property("customer.account_status", th.StringType),
        th.Property("customer.account_type", th.StringType),
        th.Property("customer.currency_code", th.StringType),
        th.Property("customer.descriptive_name", th.StringType),
        th.Property("customer.engine_id", th.StringType),
        th.Property("customer.id", th.StringType),
        th.Property("customer.manager", th.BooleanType),
        th.Property("customer.resource_name", th.StringType),
        th.Property("customer.status", th.StringType),

        # Segments
        th.Property("segments.ad_network_type", th.StringType),
        th.Property("segments.conversion_action", th.StringType),
        th.Property("segments.conversion_action_category", th.StringType),
        th.Property("segments.conversion_action_name", th.StringType),
        th.Property("segments.date", th.StringType),
        th.Property("segments.device", th.StringType),

        # Metrics
        th.Property("metrics.all_conversions", th.NumberType),
        th.Property("metrics.all_conversions_by_conversion_date", th.NumberType),
        th.Property("metrics.all_conversions_value", th.NumberType),
        th.Property("metrics.all_conversions_value_by_conversion_date", th.NumberType),
        th.Property("metrics.client_account_conversions", th.NumberType),
        th.Property("metrics.client_account_conversions_value", th.NumberType),
        th.Property("metrics.client_account_view_through_conversions", th.NumberType),
        th.Property("metrics.conversions", th.NumberType),
        th.Property("metrics.conversions_by_conversion_date", th.NumberType),
        th.Property("metrics.conversions_value", th.NumberType),
        th.Property("metrics.conversions_value_by_conversion_date", th.NumberType),
        th.Property("metrics.cross_device_conversions", th.NumberType),
        th.Property("metrics.cross_device_conversions_value", th.NumberType),
        th.Property("metrics.value_per_all_conversions", th.NumberType),
        th.Property("metrics.value_per_all_conversions_by_conversion_date", th.NumberType),
        th.Property("metrics.value_per_conversion", th.NumberType),
        th.Property("metrics.value_per_conversions_by_conversion_date", th.NumberType)
    ).to_dict()

    def get_query(self) -> str:
        return f"""
        SELECT
            campaign.bidding_strategy,
            campaign.campaign_budget,
            campaign.end_date,
            campaign.engine_id,
            campaign.id,
            campaign.labels,
            campaign.last_modified_time,
            campaign.name,
            campaign.resource_name,
            campaign.start_date,
            campaign.status,
            campaign_budget.amount_micros,
            customer.account_status,
            customer.account_type,
            customer.currency_code,
            customer.descriptive_name,
            customer.engine_id,
            customer.id,
            customer.manager,
            customer.resource_name,
            customer.status,
            segments.ad_network_type,
            segments.conversion_action,
            segments.conversion_action_category,
            segments.conversion_action_name,
            segments.date,
            segments.device,
            metrics.all_conversions,
            metrics.all_conversions_by_conversion_date,
            metrics.all_conversions_value,
            metrics.all_conversions_value_by_conversion_date,
            metrics.client_account_conversions,
            metrics.client_account_conversions_value,
            metrics.client_account_view_through_conversions,
            metrics.conversions,
            metrics.conversions_by_conversion_date,
            metrics.conversions_value,
            metrics.conversions_value_by_conversion_date,
            metrics.cross_device_conversions,
            metrics.cross_device_conversions_value,
            metrics.value_per_all_conversions,
            metrics.value_per_all_conversions_by_conversion_date,
            metrics.value_per_conversion,
            metrics.value_per_conversions_by_conversion_date
        FROM campaign
        {self.segments_date_filter()}
        """.strip() 