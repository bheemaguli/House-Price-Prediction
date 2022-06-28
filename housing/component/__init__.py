import os
from datetime import datetime

ROOT_DIR=os.getcwd()
CONFIG_DIR='config'
CONFIG_FILENAME='config,yaml'
CONFIG_FILEPATH=os.path.join(ROOT_DIR, CONFIG_DIR, CONFIG_FILENAME)

CURRENT_TIMESTAMP=datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"