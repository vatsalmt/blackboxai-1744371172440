import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List, Union
from config import Config
from logger import logger

class ThreatIntelClient:
    """Client for interacting with multiple threat intelligence APIs."""
    
    def __init__(self):
        """Initialize the threat intelligence client."""
        self.session = requests.Session()
        self.timeout = 30  # Default timeout in seconds
    
    def query_tool1(self, query: str) -> Dict[str, Any]:
        """Query the first threat intelligence API."""
        try:
            headers = {'Authorization': f'Bearer {Config.TOOL1_API_KEY}'}
            response = self.session.get(
                f'{Config.TOOL1_BASE_URL}/search',
                params={'query': query},
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return {
                'source': 'tool1',
                'status': 'success',
                'data': response.json()
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Error querying Tool 1: {str(e)}")
            return {
                'source': 'tool1',
                'status': 'error',
                'error': str(e)
            }

    def query_tool2(self, query: str) -> Dict[str, Any]:
        """Query the second threat intelligence API."""
        try:
            headers = {'X-API-Key': Config.TOOL2_API_KEY}
            response = self.session.get(
                f'{Config.TOOL2_BASE_URL}/lookup',
                params={'q': query},
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return {
                'source': 'tool2',
                'status': 'success',
                'data': response.json()
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Error querying Tool 2: {str(e)}")
            return {
                'source': 'tool2',
                'status': 'error',
                'error': str(e)
            }

    def query_tool3(self, query: str) -> Dict[str, Any]:
        """Query the third threat intelligence API."""
        try:
            headers = {'Authorization': f'Key {Config.TOOL3_API_KEY}'}
            response = self.session.get(
                f'{Config.TOOL3_BASE_URL}/investigate',
                params={'indicator': query},
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return {
                'source': 'tool3',
                'status': 'success',
                'data': response.json()
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Error querying Tool 3: {str(e)}")
            return {
                'source': 'tool3',
                'status': 'error',
                'error': str(e)
            }

    def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Search across all threat intelligence sources concurrently.
        
        Args:
            query: The indicator to search for (IP, domain, hash, etc.)
            
        Returns:
            List of results from all sources
        """
        results = []
        
        # Validate configuration before making any API calls
        missing_keys = Config.validate_config()
        if missing_keys:
            logger.error(f"Missing API keys: {', '.join(missing_keys)}")
            return [{'status': 'error', 'error': f"Missing API keys: {', '.join(missing_keys)}"}]

        # Create a list of query functions to execute
        query_functions = [
            (self.query_tool1, query),
            (self.query_tool2, query),
            (self.query_tool3, query)
        ]

        # Execute queries concurrently
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_query = {
                executor.submit(func, q): f"Tool {i+1}"
                for i, (func, q) in enumerate(query_functions)
            }

            for future in as_completed(future_to_query):
                tool_name = future_to_query[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.error(f"Error in {tool_name}: {str(e)}")
                    results.append({
                        'source': tool_name.lower().replace(' ', ''),
                        'status': 'error',
                        'error': str(e)
                    })

        return results
