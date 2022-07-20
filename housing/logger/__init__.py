import logging
from datetime import datetime
import os

LOG_DIR="logs"
LOG_TIMESTAMP=f"{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}"

def get_log_file_name(current_time_stamp):
    return f"log_{current_time_stamp}.log"

LOG_FIMENAME=get_log_file_name(current_time_stamp=LOG_TIMESTAMP)

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILEPATH=os.path.join(LOG_DIR, LOG_FIMENAME)

logging.basicConfig(
    filename=LOG_FILEPATH,
    filemode='a',
    format='[%(asctime)s] %(levelname)s - %(processName)s - %(threadName)s - %(name)s  - %(filename)s - %(funcName)s - %(lineno)d - %(message)s',
    level=logging.INFO
)