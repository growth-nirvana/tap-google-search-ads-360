from singer_sdk.streams.core import Stream
from singer_sdk.helpers.jsonpath import extract_jsonpath
from datetime import datetime, timedelta
from typing import Iterable
import re
from datetime import datetime, timedelta

from tap_search_ads.client import SA360Client


def to_snake_case(name: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

def flatten_dict(d: dict, parent_key: str = '', sep: str = '.') -> dict:
    items = []
    for k, v in d.items():
        k = to_snake_case(k)
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def to_yyyy_mm_dd(date_str: str) -> str:
    """Convert any date string to YYYY-MM-DD format."""
    if not date_str:
        return date_str
    # If it's already in YYYY-MM-DD format, return as is
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return date_str
    # If it has a time component, split on T and take the date part
    if 'T' in date_str:
        return date_str.split('T')[0]
    # If it's a datetime object, convert to string
    if isinstance(date_str, datetime):
        return date_str.strftime('%Y-%m-%d')
    # If it's a date object, convert to string
    if isinstance(date_str, datetime.date):
        return date_str.strftime('%Y-%m-%d')
    return date_str


class SearchAdsStream(Stream):
    records_jsonpath = "$.results[*]"
    replication_key = None
    client: SA360Client

    def __init__(self, tap, customer_ids: list[str], *args, **kwargs):
        super().__init__(tap=tap, *args, **kwargs)
        self.customer_ids = customer_ids
        self.client = SA360Client(self)

    def get_start_date(self) -> str:
        start_date = self.config.get("start_date")
        if start_date:
            return to_yyyy_mm_dd(start_date)
        today = datetime.utcnow().date()
        return str(today - timedelta(days=30))

    def get_end_date(self) -> str:
        return to_yyyy_mm_dd(str(datetime.utcnow().date()))

    def segments_date_filter(self) -> str:
        """Returns a GAQL WHERE clause with a required finite date range filter."""
        start_date = self.get_start_date()
        end_date = self.get_end_date()
        return f"WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'"

    def get_query(self) -> str:
        raise NotImplementedError("Subclasses must implement `get_query()`")

    def get_records(self, context: dict) -> Iterable[dict]:
        query = self.get_query()
        for customer_id in self.customer_ids:
            response = self.client.generate_report(query, customer_id)
            for row in extract_jsonpath(self.records_jsonpath, input=response):
                yield flatten_dict(row)
