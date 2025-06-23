# Understanding the Tap Command Syntax

This guide explains the syntax and components of the tap-search-ads command.

## Basic Command

```bash
tap-search-ads --config config.json --catalog catalog.json --state state.json > output.json
```

## Command Breakdown

### 1. Main Command
```bash
tap-search-ads
```
- This is the main executable that runs the Singer tap
- It's installed when you run `pip install -e .`
- The name comes from the `name` field in `tap.py`

### 2. Configuration File
```bash
--config config.json
```
- Specifies the file containing your credentials and settings
- Required for authentication and basic configuration
- Contains:
  ```json
  {
      "client_id": "your_client_id",
      "client_secret": "your_client_secret",
      "refresh_token": "your_refresh_token",
      "login_customer_id": "your_login_customer_id",
      "customer_ids": "customer_id1,customer_id2",
      "start_date": "2024-01-01"  // Optional
  }
  ```

### 3. Catalog File
```bash
--catalog catalog.json
```
- Defines the data structure and available streams
- Generated using: `tap-search-ads --config config.json --discover > catalog.json`
- Contains:
  - Schema definitions for each stream
  - Field types and properties
  - Stream metadata
  - Selection flags for which streams to sync

### 4. State File
```bash
--state state.json
```
- Tracks the sync progress
- Enables incremental syncs
- Gets updated after each successful sync
- Contains:
  - Last successful sync timestamp
  - Bookmark values for each stream
  - Sync status information

### 5. Output Redirection
```bash
> output.json
```
- The `>` operator redirects standard output to a file
- Creates or overwrites output.json
- Contains the actual data in Singer format:
  ```json
  {"type": "RECORD", "stream": "ad_groups", "record": {...}}
  {"type": "SCHEMA", "stream": "ad_groups", "schema": {...}}
  {"type": "STATE", "value": {...}}
  ```

## Common Use Cases

### 1. First-time Run
```bash
# Generate catalog
tap-search-ads --config config.json --discover > catalog.json

# Run the tap
tap-search-ads --config config.json --catalog catalog.json --state state.json > output.json
```

### 2. Incremental Sync
```bash
# Uses existing state.json to continue from last sync
tap-search-ads --config config.json --catalog catalog.json --state state.json > output.json
```

### 3. Full Refresh
```bash
# Remove state.json to force full sync
rm state.json
tap-search-ads --config config.json --catalog catalog.json --state state.json > output.json
```

## Troubleshooting

### Common Issues

1. **Missing Files**
   - Ensure all required files exist (config.json, catalog.json)
   - Check file permissions

2. **Invalid Configuration**
   - Verify all required fields in config.json
   - Check credential validity

3. **State File Issues**
   - If sync fails, try removing state.json
   - Ensure state.json is writable

4. **Output File**
   - Check disk space
   - Verify write permissions
   - Consider using a different output file name

## Best Practices

1. **File Management**
   - Keep config.json secure (contains credentials)
   - Back up state.json regularly
   - Use meaningful names for output files

2. **Running the Tap**
   - Always use the same catalog.json for consistency
   - Keep state.json for incremental syncs
   - Monitor output file size

3. **Error Handling**
   - Check exit codes
   - Review error messages
   - Keep logs for debugging 