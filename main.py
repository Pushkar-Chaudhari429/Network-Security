from newtork_security.components.data_ingestion import DataIngestion
from newtork_security.components.data_validation import DataValidation
from newtork_security.logging.logger import logging
from newtork_security.entity.config_entity import DataIngestionConfig,DataValidationConfig
from newtork_security.entity.config_entity import TrainingPipelineConfig

if __name__=="__main__":
    dataIngestion=DataIngestion(DataIngestionConfig(TrainingPipelineConfig()))
    training_pipeline_config=TrainingPipelineConfig()
    dataArtifact=dataIngestion.initiate_data_ingestion()
    logging.info("initiated data ingestion component")
    print(f"Training file path: {dataArtifact.training_file_path}")
    print(f"Testing file path: {dataArtifact.testing_file_path}")
    logging.info("Data ingestion component completed successfully")
    logging.info("initiated data validation component")
    data_validation_config=DataValidationConfig(training_pipeline_config)
    data_validation=DataValidation(data_validation_config,dataArtifact)
    data_validation_artifacts=data_validation.initiate_data_validation()
    logging.info("initiated data validation component")
    print(data_validation_artifacts)

