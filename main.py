from newtork_security.components.data_ingestion import DataIngestion
from newtork_security.logging.logger import logging
from newtork_security.exception.exception import NetworkSecurityException
from newtork_security.entity.config_entity import DataIngestionConfig
from newtork_security.entity.config_entity import TrainingPipelineConfig

if __name__=="__main__":
    dataIngestion=DataIngestion(DataIngestionConfig(TrainingPipelineConfig()))
    dataArtifact=dataIngestion.initiate_data_ingestion()
    logging.info("initiated data ingestion component")
    print(f"Training file path: {dataArtifact.training_file_path}")
    print(f"Testing file path: {dataArtifact.testing_file_path}")
    logging.info("Data ingestion component completed successfully")
