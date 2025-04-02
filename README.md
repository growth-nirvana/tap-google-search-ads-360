
# Tap Google Search Ads 360

A Singer tap for integrating Google Search Ads 360 data with external systems.

## Overview

This project implements a **Singer tap** to extract data from **Google Search Ads 360** using their API. It supports multiple customer IDs, automatic date filtering, and more.

## Features

- Retrieve data from Google Search Ads 360 for ad groups, campaigns, and customers.
- Supports date filtering for each stream.
- Easily configurable using `config.json`.

## Installation

### Prerequisites

Ensure you have Python 3.6+ and pip installed.

### Clone the repository

```bash
git clone https://github.com/growth-nirvana/tap-google-search-ads-360.git
cd tap-google-search-ads-360
```

### Setup a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scriptsctivate`
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configuration

Copy the example config file to `config.json`:

```bash
cp config.json.example config.json
```

Edit the `config.json` file with your credentials and configuration details.

## Running the Tap

To run the tap and start syncing data, use:

```bash
tap-search-ads --config config.json --catalog catalog.json --discover  # For discovering streams
tap-search-ads --config config.json --catalog catalog.json  # For syncing data
```

## License

This project is licensed under the MIT License.
