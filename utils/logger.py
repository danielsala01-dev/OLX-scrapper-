"""
Konfiguracja loggingu
Zapisuje logi do konsoli i pliku
"""

import logging
from datetime import datetime

def setup_logger(name):
    """
    Stwórz logger
    
    Args:
        name: nazwa loggera
    
    Returns:
        logger object
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Format logów
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler do konsoli
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler do pliku
    file_handler = logging.FileHandler('app.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
