from housing.pipeline.pipeline import Pipeline
from housing.exception import HousingException
from housing.logger import logging
from housing.config.config import Configuartion
import os
def main():
    try:
        logging.info(f"Project run started")
        config_path = os.path.join("config","config.yaml")
        pipeline = Pipeline(Configuartion(config_file_path=config_path))        
        pipeline.run_pipeline()
        logging.info(f"Project run completed")
    except Exception as e:
        logging.error(f"{e}")
        print(e)



if __name__=="__main__":
    main()