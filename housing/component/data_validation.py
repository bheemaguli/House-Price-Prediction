from inspect import trace
from urllib.parse import scheme_chars
from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from housing.config.config import read_yaml_file
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import os,sys
import pandas  as pd
import json

class DataValidation:
    

    def __init__(self, data_validation_config:DataValidationConfig,
        data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info(f"{'='*20}Data Validation log started.{'='*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise HousingException(e,sys) from e


    def get_train_and_test_df(self):
        try:
            logging.info(f"Proceeding to get train and test datasets for validations.")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            logging.info(f"Train and test datasets extracted as dataframes.")
            return train_df,test_df
        except Exception as e:
            raise HousingException(e,sys) from e


    def is_train_test_file_exists(self)->bool:
        try:
            logging.info("Checking if training and test file is available")
            is_train_file_exist = False
            is_test_file_exist = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)

            is_available =  is_train_file_exist and is_test_file_exist

            logging.info(f"Is train and test file exists? -> {is_available}")
            
            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path
                testing_file = self.data_ingestion_artifact.test_file_path
                message=f"Training file: {training_file} or Testing file: {testing_file}" \
                    "is not present"
                raise Exception(message)

            return is_available
        except Exception as e:
            raise HousingException(e,sys) from e

    
    def validate_dataset_schema(self)->bool:
        try:
            logging.info(f"Checking if training and test file fits the schema.")
            validation_status = False
            
            scheme_file_path = self.data_validation_config.schema_file_path
            schema_values = read_yaml_file(file_path=scheme_file_path)
            
            train_df,test_df = self.get_train_and_test_df()
            
            conditions = {'train_df_col_count':False,
                          'test_df_col_count':False,
                          'train_df_ocean_val_validity':False,
                          'test_df_ocean_val_validity':False}
            
            if len(schema_values['columns'].keys()) == len(train_df.columns):
                conditions['train_df_col_count'] = True
                
            if len(schema_values['columns'].keys()) == len(test_df.columns):
                conditions['test_df_col_count'] = True
                
            if all(list(train_df['ocean_proximity'].isin(schema_values['domain_value']['ocean_proximity']))):
                conditions['train_df_ocean_val_validity'] = True
                
            if all(list(test_df['ocean_proximity'].isin(schema_values['domain_value']['ocean_proximity']))):
                conditions['test_df_ocean_val_validity'] = True
                        
            if all(list(conditions.values())):
                validation_status = True
            
            logging.info(f"Is the datasets as per schema? -> {validation_status}")
            
            return validation_status 
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_and_save_data_drift_report(self):
        try:
            logging.info(f"Proceeding to get train and test datasets drift analysis.")
            profile = Profile(sections=[DataDriftProfileSection()])

            train_df,test_df = self.get_train_and_test_df()

            profile.calculate(train_df,test_df)

            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            with open(report_file_path,"w") as report_file:
                json.dump(report, report_file, indent=6)
            logging.info(f"Dataset drift analysis completed.")
            return report
        except Exception as e:
            raise HousingException(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            logging.info(f"Proceeding to save drift analysis reports.")
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df,test_df = self.get_train_and_test_df()
            dashboard.calculate(train_df,test_df)

            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(report_page_file_path)
            logging.info(f"Dataset drift analysis report saved successfully.")
        except Exception as e:
            raise HousingException(e,sys) from e

    def is_data_drift_found(self)->bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            
            report_page_file_path = self.data_validation_config.report_page_file_path
            report_file_exists = os.path.exists(report_page_file_path)
            
            logging.info(f"Does drift analysis report exists? -> {report_file_exists}")
            return report_file_exists
        except Exception as e:
            raise HousingException(e,sys) from e

    def initiate_data_validation(self)->DataValidationArtifact :
        try:
            self.is_train_test_file_exists()
            self.validate_dataset_schema()

            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                is_validated=self.is_data_drift_found(),
                message="Data Validation performed successully."
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def __del__(self):
        logging.info(f"{'='*20}Data Validation log completed.{'='*20}")