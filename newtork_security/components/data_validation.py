from newtork_security.entity.data_ingestion_artifacts import DataValidationArtifact,DataIngestionArtifact
from newtork_security.entity.config_entity import DataValidationConfig
from newtork_security.exception.exception import NetworkSecurityException
from newtork_security.logging.logger import logging
from newtork_security.constant.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import pandas as pd
from newtork_security.utils.main_utils.utils import read_yaml_file,write_yaml_file
import os
import sys


class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,
                 data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self._schema_config['columns'])
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Dataframe has columns: {dataframe.columns}")
            return len(dataframe.columns)==number_of_columns
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def detect_dataset_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                p_value=ks_2samp(d1,d2).pvalue
                if p_value<=threshold:
                    is_found=True
                    status=False
                else:
                    is_found=False
                report.update({column:{
                    "p_value":float(p_value),
                    "drift_status":is_found
                }})
            report_file_path=self.data_validation_config.drift_report_file_path
            dir_path=os.path.dirname(report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=report_file_path,content=report)
            return status
        except Exception as e:

            raise NetworkSecurityException(e,sys)

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.training_file_path
            test_file_path=self.data_ingestion_artifact.testing_file_path
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)
            status=self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                raise Exception(f"Train dataframe does not have all columns")
            status=self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                raise Exception(f"Test dataframe does not have all columns")
            
            status=self.detect_dataset_drift(train_dataframe,test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            invalid_dir_path=os.path.dirname(self.data_validation_config.invalid_train_file_path)
            os.makedirs(invalid_dir_path,exist_ok=True)
            if status:
                train_dataframe.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
                test_dataframe.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)
            else:
                train_dataframe.to_csv(self.data_validation_config.invalid_train_file_path,index=False,header=True)
                test_dataframe.to_csv(self.data_validation_config.invalid_test_file_path,index=False,header=True)
            data_validation_artifact=DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None if status else self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=None if status else self.data_validation_config.invalid_test_file_path,
                valid_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)