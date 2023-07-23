import logging
import os
from datetime import datetime




# 1. set the folder where logs will be stored:( logs-> error_folder-> error_files )

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" # format for the log directory
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE) # will make logs/LOG_FILE in cwd
os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE) # will create this file inside the logs_path directory

# 2. setting the basic configuration of saving the files of multiple Levels

logging.basicConfig(
    filename = LOG_FILE_PATH, # in already created LOG_FILE in logs_path
    format =  "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s", # insige the file
    level = logging.INFO, # level in CAPS
)

if __name__ == "__main__":
    logging.info("Logging has started") # %(message)s