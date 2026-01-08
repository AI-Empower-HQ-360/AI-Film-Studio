"""Logging utility for AI Film Studio"""
import logging
import sys

def setup_logger(name: str, log_level: str = "INFO") -> logging.Logger:
    """Setup logger with specified name and level"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level))
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    return logger
