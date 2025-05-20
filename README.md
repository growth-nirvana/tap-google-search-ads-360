# Tap Google Search Ads 360

A Singer tap for extracting data from Google Search Ads 360 (SA360).

## Setup

1. Create a Python virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install the tap:
```bash
pip install -e .
```

3. Create a config.json file with your credentials:
```json
{
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "refresh_token": "your_refresh_token",
    "login_customer_id": "your_login_customer_id",
    "customer_ids": "customer_id1,customer_id2",
    "start_date": "2024-01-01"  # Optional
}
```

## Usage

### 1. Generate Catalog

First, generate a catalog file that defines the data structure:

```bash
tap-search-ads --config config.json --discover > catalog.json
```

The catalog.json file contains:
- Schema definitions for each stream (table)
- Available fields and their data types
- Stream metadata and configuration

### 2. Run the Tap

To extract data and output to a file:

```bash
tap-search-ads --config config.json --catalog catalog.json --state state.json > output.json
```

Command breakdown:
- `tap-search-ads`: The main command
- `--config config.json`: Configuration file with credentials
- `--catalog catalog.json`: Data structure definition
- `--state state.json`: Tracks sync progress for incremental syncs
- `> output.json`: Redirects output to a file

### Command Components

#### config.json
Contains your SA360 credentials and settings:
- `client_id`: OAuth client ID
- `client_secret`: OAuth client secret
- `refresh_token`: OAuth refresh token
- `login_customer_id`: Your SA360 login customer ID
- `customer_ids`: Comma-separated list of customer IDs to sync
- `start_date`: (Optional) Start date for historical data

#### catalog.json
Defines the data structure:
- Available streams (tables)
- Field definitions and types
- Stream properties and settings
- Generated using the `--discover` flag

#### state.json
Tracks sync progress:
- Last successful sync for each stream
- Enables incremental syncs
- Updated after each successful sync

#### output.json
Contains the extracted data:
- Records in Singer format
- One record per line
- JSON format with schema information

## Available Streams

The tap includes the following streams:
- Ad Groups
- Ad Group Ads
- Ad Group Conversions
- Ad Group Conversion Actions
- Campaigns
- Campaign Conversions
- Conversion Actions
- Customers
- Floodlight Activities
- Keywords
- Performance Max Conversions

## Development

To add new streams or modify existing ones:
1. Create a new stream class in `tap_search_ads/streams/`
2. Inherit from `SearchAdsStream`
3. Define the schema and query
4. Add the stream to `tap.py`

## License

This project is licensed under the MIT License.
