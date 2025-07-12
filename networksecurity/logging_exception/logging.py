'''
Log the entire execution process including any errors
'''
import logging
import os 
from datetime import datetime

#Create a timestamped log file 
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

#Combines the current working directory, a folder called logs, and the log filename into one pat
logs_dir = os.path.join(os.getcwd(), 'logs')

#Creates the log directory
os.makedirs(logs_dir, exist_ok=True)

#Specifies log file path
LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)

#Set up the logger
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    #Only logs messages at INFO level or higher (e.g., WARNING, ERROR)
    level= logging.INFO
)

# To test the run
'''
if __name__ == '__main__':
    logging.info("Logging has started")
'''
