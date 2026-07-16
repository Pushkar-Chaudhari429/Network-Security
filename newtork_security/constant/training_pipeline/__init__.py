import os
import sys
import pandas as pd
import numpy as np

TARGET_COLUMN:str="Result"
PIPELINE_NAME:str="Network_Security"
ARTIFACTS_DIR:str="artifacts"
FILE_NAME:str="phisingData.csv"

DATA_INGESTION_TRAINING_FILE_NAME:str="train.csv"
DATA_INGESTION_TESTING_FILE_NAME:str="test.csv"

DATA_INGESTION_COLLECTION_NAME:str="Network_security"
DATA_INGESTION_DATABASE_NAME:str="Pushkar_db"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2

SCHEMA_FILE_PATH=os.path.join("data_schema","schema.yaml")

DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_VALID_DIR:str="validated"
DATA_VALIDATION_INVALID_DIR:str="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str="report.yaml"