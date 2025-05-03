import sys
from phishnet.logging.logger import logging
from phishnet.exception.exception import PhishnetException
from phishnet.components.data_validation import DataValidation
from phishnet.components.data_ingestion import DataIngestion
from phishnet.entity.config_entity import DataIngestionConfig, DataValidationConfig
from phishnet.entity.config_entity import TrainingPipelineConfig

if __name__=='__main__':
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        
        # data ingestion
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)
        logging.info("Data Initiation Complete")

        # data validation
        datavalidationconfig = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestionartifact, datavalidationconfig)
        logging.info("Initiate the data validation")
        datavalidationartifact = data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
        print(datavalidationartifact)

    except Exception as e:
           # Raise custom exception with error details
           raise PhishnetException(e,sys)