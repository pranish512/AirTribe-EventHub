import time
import logging
import os
from pathlib import Path

# Configure logger with file handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create logs directory if it doesn't exist
logs_dir = Path(__file__).resolve().parent.parent / 'logs'
logs_dir.mkdir(exist_ok=True)

# File handler configuration
log_file = logs_dir / 'eventhub_debugger.logs'
file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Console handler configuration
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger (avoid duplicates)
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


class RequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        # Log incoming request
        breakpoint()
        logger.info(f"[REQUEST] {request.method} {request.path} - Query Params: {dict(request.GET)}")
        
        response = self.get_response(request)
        duration = time.time() - start_time
        
        # Log response details
        logger.info(f"[RESPONSE] {request.method} {request.path} - Status: {response.status_code} - Duration: {duration:.3f}s")
        
        # Log errors or warnings for non-2xx status codes
        if response.status_code >= 400:
            logger.warning(f"[ERROR] {request.method} {request.path} - Status: {response.status_code}")
        
        return response
