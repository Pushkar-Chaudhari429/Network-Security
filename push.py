import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()
import pymongo

MONGODB_URL=os.getenv("MONGO_DB_URL")
print(MONGODB_URL)

import certifi
ca=certifi.where()

import pandas as pd
import numpy as np
from newtork_security.exception.exception import NetworkSecurityException
from newtork_security.logging.logger import logging

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def cv_to_json_converter(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:  
            raise NetworkSecurityException(e,sys)
    
    def insert_data_mongo(self,records,database,collection):
        try:
            self.database=database
            self.records=records
            self.collection=collection
            self.mongo_client=pymongo.MongoClient(MONGODB_URL,tlsCAFile=ca)
            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__=="__main__":
    try:
        File_path="Network_data\phisingData.csv"
        database="Pushkar_db"
        collection="Network_security"
        obj=NetworkDataExtract()
        records=obj.cv_to_json_converter(File_path)
        print(records)
        number_of_records=obj.insert_data_mongo(records,database,collection)
        print(f"Total number of records inserted in database {database} and collection {collection} is {number_of_records}")
    except Exception as e:
        raise NetworkSecurityException(e,sys)