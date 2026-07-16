import logging
import sys

def setup_logger(log_file: str = "logs.txt") -> logging.Logger:
    """Sets up and returns a logger that logs to both console and a file."""
    logger = logging.getLogger("AutoSlideCapture")
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # File handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

app_logger = setup_logger()
