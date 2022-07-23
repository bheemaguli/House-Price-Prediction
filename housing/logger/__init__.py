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

def get_log_dataframe(file_path):
    data=[]
    with open(file_path) as log_file:
        for line in log_file.readlines():
            data.append(line.split("^;"))

    log_df = pd.DataFrame(data)
    columns=["Time stamp","Log Level","line number","file name","function name","message"]
    log_df.columns=columns
    
    log_df["log_message"] = log_df['Time stamp'].astype(str) +":$"+ log_df["message"]

    return log_df[["log_message"]]