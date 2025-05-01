import sys
from phishnet.logging.logger import logging
from phishnet.exception.exception import PhishnetException
from phishnet.components.data_ingestion import DataIngestion
from phishnet.entity.config_entity import DataIngestionConfig
from phishnet.entity.config_entity import TrainingPipelineConfig

if __name__=='__main__':
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        
        logging.info("Initiate the data ingestion")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()

        print(dataingestionartifact)

    except Exception as e:
           # Raise custom exception with error details
           raise PhishnetException(e,sys)