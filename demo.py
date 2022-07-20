from housing.pipeline.pipeline import Pipeline
from housing.exception import HousingException
from housing.logger import logging
from housing.config.config import Configuartion
import os
def main():
    try:
        logging.info(f"{'*'*50}Project run started{'*'*50}")
        config_path = os.path.join("config","config.yaml")
        pipeline = Pipeline(Configuartion(config_file_path=config_path))
        pipeline.start()
    except Exception as e:
        logging.error(f"{e}")
        print(e)



if __name__=="__main__":
    main()
    logging.info(f"{'*'*50}Project run completed{'*'*50}")