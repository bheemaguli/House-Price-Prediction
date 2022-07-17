import logging
from datetime import datetime
import os

LOG_DIR="project_logs"
LOG_TIMESTAMP=f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
LOG_FIMENAME=f"log_{LOG_TIMESTAMP}.log"

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILEPATH=os.path.join(LOG_DIR, LOG_FIMENAME)

logging.basicConfig(
    filename=LOG_FILEPATH,
    filemode='a',
    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)