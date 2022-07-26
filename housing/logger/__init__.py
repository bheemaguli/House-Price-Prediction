import logging
from datetime import datetime
from housing.constant import get_current_time_stamp
import os
import pandas as pd

LOG_DIR="logs"

def get_log_file_name():
    return f"log_{get_current_time_stamp()}.log"

LOG_FIMENAME=get_log_file_name()

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILEPATH=os.path.join(LOG_DIR, LOG_FIMENAME)

logging.basicConfig(
    filename=LOG_FILEPATH,
    filemode='w',
    format='[%(asctime)s] %(levelname)s - %(filename)s - %(lineno)d - %(funcName)s - %(message)s',
    level=logging.INFO
)