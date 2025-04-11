import logging
from rich.logging import RichHandler

def setup_logger():
    """Configure and return a logger instance."""
    
    # Create logger
    logger = logging.getLogger('threat_intel')
    logger.setLevel(logging.INFO)
    
    # Remove any existing handlers
    if logger.handlers:
        logger.handlers.clear()
    
    # Create rich handler for better console output
    handler = RichHandler(rich_tracebacks=True)
    handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger

# Create a logger instance
logger = setup_logger()
