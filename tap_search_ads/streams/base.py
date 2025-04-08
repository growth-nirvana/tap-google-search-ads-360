from singer_sdk.streams.core import Stream
from singer_sdk.helpers.jsonpath import extract_jsonpath
from datetime import datetime, timedelta
from typing import Iterable
import re
from tap_search_ads.client import SA360Client



def to_snake_case(name: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

def flatten_dict(d: dict, parent_key: str = '', sep: str = '.') -> dict:
    items = []
    for k, v in d.items():
        k = to_snake_case(k)  # Convert keys to snake_case
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

class SearchAdsStream(Stream):
    records_jsonpath = "$.results[*]"
    replication_key = None
    client: SA360Client

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = SA360Client(self)

    def get_date_range(self) -> tuple[str, str]:
        today = datetime.utcnow().date()
        start_date = self.config.get("start_date") or str(today - timedelta(days=30))
        end_date = self.config.get("end_date") or str(today)
        return start_date, end_date

    def get_query(self) -> str:
        raise NotImplementedError("Subclasses must implement `get_query()`")

    def get_records(self, context: dict) -> Iterable[dict]:
        query = self.get_query()
        for customer_id in self.config["customer_ids"]:
            response = self.client.generate_report(query, customer_id)
            for row in extract_jsonpath(self.records_jsonpath, input=response):
                yield flatten_dict(row)