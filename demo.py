from housing.pipeline.pipeline import Pipeline
from housing.exception import HousingException
from housing.logger import logging
from housing.config.config import Configuartion
import os
def main():
    try:
        logging.info(f"Project run started")
        pipeline = Pipeline()
        pipeline.run_pipeline()
        logging.info(f"Project run completed")
    except Exception as e:
        logging.error(f"{e}")
        print(e)



if __name__=="__main__":
    main()