import logging 
import os
from datetime import datetime

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

LOGS_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

# Create a logger
logging.basicConfig(
    filename=LOGS_FILE,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Add console handler (for terminal streaming)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Attach console handler to root logger
logging.getLogger().addHandler(console_handler)

def get_logger(name):
    """
    Function to initialise logger in different scripts
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger