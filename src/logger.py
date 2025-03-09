import logging
import os
from datetime import datetime

# Define the log directory and file
log_path = os.path.join(os.getcwd(), "logs")
os.makedirs(log_path, exist_ok=True)
LOG_FILE = os.path.join(log_path, f"{datetime.now().strftime('%Y-%m-%d')}.log")

# Define the log format
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)
