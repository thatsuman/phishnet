import sys
from phishnet.logging.logger import logging
from phishnet.exception.exception import PhishnetException
from phishnet.components.data_ingestion import DataIngestion
from phishnet.components.data_validation import DataValidation
from phishnet.components.data_transformation import DataTransformation
from phishnet.components.model_trainer import ModelTrainer
from phishnet.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
from phishnet.entity.config_entity import TrainingPipelineConfig

if __name__=='__main__':
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        
        # data ingestion
        logging.info("Initiate Data Ingestion")
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)
        logging.info("Data Initiation Complete")

        # data validation
        logging.info("Initiate Data Validation")
        datavalidationconfig = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestionartifact, datavalidationconfig)
        datavalidationartifact = data_validation.initiate_data_validation()
        print(datavalidationartifact)
        logging.info("Data Validation Completed")

        # data transformation
        logging.info("Initiate Data Transformation")
        datatransformationconfig = DataTransformationConfig(trainingpipelineconfig)
        data_transformation = DataTransformation(datavalidationartifact, datatransformationconfig)
        datatransformationartifact = data_transformation.initiate_data_transformation()
        print(datatransformationartifact)
        logging.info("Data Tranformation Completed")

        # model training
        logging.info("Model Training started")
        modeltrainerconfig = ModelTrainerConfig(trainingpipelineconfig)
        model_trainer = ModelTrainer(model_trainer_config = modeltrainerconfig,
                                    data_transformation_artifact = datatransformationartifact)
        modeltrainerartifact = model_trainer.initiate_model_trainer()

        logging.info("Model Training artifact created")

    except Exception as e:
           # Raise custom exception with error details
           raise PhishnetException(e,sys)