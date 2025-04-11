# Threat Intelligence Aggregator

A Python-based tool that aggregates results from multiple threat intelligence sources into a single interface. This tool allows you to search across multiple threat intelligence APIs simultaneously and view consolidated results.

## Features

- Concurrent querying of multiple threat intelligence sources
- Unified interface for searching across all sources
- Rich console output with formatted tables
- Optional JSON output format
- Robust error handling and logging
- Easy configuration through environment variables

## Installation

1. Clone the repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
3. Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```
4. Edit the `.env` file and add your API keys:
```
TOOL1_API_KEY=your_tool1_api_key_here
TOOL2_API_KEY=your_tool2_api_key_here
TOOL3_API_KEY=your_tool3_api_key_here
```

## Usage

Basic usage:
```bash
python main.py <indicator>
```

Example searching for an IP address:
```bash
python main.py 8.8.8.8
```

Output results in JSON format:
```bash
python main.py --json 8.8.8.8
```

## Output Formats

### Table Format (Default)
The tool will display results in a formatted table showing:
- Source name
- Query status
- Detailed results or error messages

### JSON Format
Use the `--json` flag to output results in JSON format, useful for:
- Parsing results programmatically
- Integrating with other tools
- Storing results for later analysis

## Error Handling

The tool handles various error scenarios:
- Missing API keys
- API connection failures
- Invalid responses
- Timeout issues

Each error is logged and displayed in the results, allowing other sources to continue functioning even if one fails.

## Configuration

All configuration is done through environment variables:

Required:
- `TOOL1_API_KEY`: API key for the first threat intelligence source
- `TOOL2_API_KEY`: API key for the second threat intelligence source
- `TOOL3_API_KEY`: API key for the third threat intelligence source

Optional:
- `TOOL1_BASE_URL`: Custom base URL for the first API
- `TOOL2_BASE_URL`: Custom base URL for the second API
- `TOOL3_BASE_URL`: Custom base URL for the third API

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

MIT License - feel free to use this tool for any purpose.
