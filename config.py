import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class to manage API keys and base URLs."""
    
    # API Keys (loaded from environment variables)
    TOOL1_API_KEY = os.getenv('TOOL1_API_KEY')
    TOOL2_API_KEY = os.getenv('TOOL2_API_KEY')
    TOOL3_API_KEY = os.getenv('TOOL3_API_KEY')
    
    # Base URLs for each API
    TOOL1_BASE_URL = os.getenv('TOOL1_BASE_URL', 'https://api.tool1.com/v1')
    TOOL2_BASE_URL = os.getenv('TOOL2_BASE_URL', 'https://api.tool2.com/v1')
    TOOL3_BASE_URL = os.getenv('TOOL3_BASE_URL', 'https://api.tool3.com/v1')

    @classmethod
    def validate_config(cls):
        """Validate that all required API keys are present."""
        missing_keys = []
        
        if not cls.TOOL1_API_KEY:
            missing_keys.append('TOOL1_API_KEY')
        if not cls.TOOL2_API_KEY:
            missing_keys.append('TOOL2_API_KEY')
        if not cls.TOOL3_API_KEY:
            missing_keys.append('TOOL3_API_KEY')
            
        return missing_keys
