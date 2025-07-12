import logging
import os
from datetime import datetime

### Log the entire execution process including any errors ###

# Create a timestamped log file
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Combine current working directory, a folder called 'logs', and the log filename
logs_dir = os.path.join(os.getcwd(), 'logs')

# Create the log directory if it doesn't exist
os.makedirs(logs_dir, exist_ok=True)

# Full path to the log file
LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)

# Set up the logger
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    force=True  # Python 3.8+; remove if using older versions
)

# Example usage
if __name__ == '__main__':
    logging.info("Logging has started")