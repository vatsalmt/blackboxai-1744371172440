import argparse
import json
from rich.console import Console
from rich.table import Table
from config import Config
from logger import logger
from threat_intel_client import ThreatIntelClient

def create_result_table(results):
    """Create a formatted table for displaying results."""
    table = Table(title="Threat Intelligence Results")
    
    # Add columns
    table.add_column("Source", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details", style="white")

    # Add rows
    for result in results:
        source = result.get('source', 'Unknown')
        status = result.get('status', 'Unknown')
        
        if status == 'success':
            details = json.dumps(result.get('data', {}), indent=2)
            status_style = "green"
        else:
            details = result.get('error', 'No details available')
            status_style = "red"
            
        table.add_row(source, f"[{status_style}]{status}[/{status_style}]", details)
    
    return table

def main():
    """Main entry point for the threat intelligence tool."""
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Query multiple threat intelligence sources for information about an indicator."
    )
    parser.add_argument(
        "query",
        help="The indicator to search for (IP address, domain, hash, etc.)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format instead of table format"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize console for rich output
    console = Console()
    
    # Validate configuration
    missing_keys = Config.validate_config()
    if missing_keys:
        console.print(f"[red]Error: Missing API keys: {', '.join(missing_keys)}[/red]")
        console.print("\nPlease set the following environment variables:")
        for key in missing_keys:
            console.print(f"  - {key}")
        return 1

    try:
        # Initialize the threat intelligence client
        client = ThreatIntelClient()
        
        # Log the search
        logger.info(f"Searching for indicator: {args.query}")
        
        # Perform the search
        results = client.search(args.query)
        
        # Output results based on format preference
        if args.json:
            # JSON output
            console.print_json(json.dumps(results, indent=2))
        else:
            # Table output
            table = create_result_table(results)
            console.print(table)
            
        # Check if any errors occurred
        if any(r.get('status') == 'error' for r in results):
            return 1
            
        return 0
        
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
