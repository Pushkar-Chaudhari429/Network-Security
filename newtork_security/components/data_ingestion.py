from newtork_security.exception.exception import NetworkSecurityException
from newtork_security.logging.logger import logging

from newtork_security.entity.config_entity import DataIngestionConfig
from newtork_security.entity.data_ingestion_artifacts import DataIngestionArtifact
import os
import sys
import pandas as pd
import pymongo
import numpy as np
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGODB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def export_collection_as_dataframe(self):
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGODB_URL)
            collection=self.mongo_client[database_name][collection_name]

            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns:
                df=df.drop("_id",axis=1)
            df.replace("na",np.nan,inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def export_data_into_feature_store(self,df:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            df.to_csv(feature_store_file_path,index=False,header=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def split_data_as_train_test(self,df:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(df,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on the dataset")
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info("Exporting training and testing data to local file system")
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)
            logging.info("training and testing datas are saved in the local file system")
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifact=DataIngestionArtifact(self.data_ingestion_config.training_file_path,self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)