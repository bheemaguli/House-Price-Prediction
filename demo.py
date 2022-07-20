from housing.pipeline.pipeline import Pipeline
from housing.exception import HousingException
from housing.logger import logging
from housing.config.config import Configuartion
import os
def main():
    try:
        logging.info(f"{'*'*50}Project run started{'*'*50}")
        pipeline = Pipeline()
        pipeline.start()
        logging.info(f"{'*'*50}Project run completed{'*'*50}")
    except Exception as e:
        logging.error(f"{e}")
        print(e)



if __name__=="__main__":
    main()