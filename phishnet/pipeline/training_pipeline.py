import os
import sys

from phishnet.exception.exception import PhishnetException
from phishnet.logging.logger import logging

from phishnet.components.data_ingestion import DataIngestion
from phishnet.components.data_validation import DataValidation
from phishnet.components.data_transformation import DataTransformation
from phishnet.components.model_trainer import ModelTrainer

from phishnet.entity.config_entity import(
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
)

from phishnet.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
)

# from phishnet.constant.training_pipeline import TRAINING_BUCKET_NAME
# from phishnet.cloud.s3_syncer import S3Sync
from phishnet.constant.training_pipeline import SAVED_MODEL_DIR


class TrainingPipeline:
    def __init__(self):
        # Initialize the training pipeline configuration
        self.trainingpipelineconfig = TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            # Create DataIngestionConfig using the pipeline config
            self.dataingestionconfig = DataIngestionConfig(training_pipeline_config=self.trainingpipelineconfig)
            logging.info("Starting data ingestion")
            # Create DataIngestion object and start ingestion
            data_ingestion = DataIngestion(data_ingestion_config=self.dataingestionconfig)
            dataingestionartifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion completed and artifact: {dataingestionartifact}")
            return dataingestionartifact
                
        except Exception as e:
            raise PhishnetException(e, sys)
        
    def start_data_validation(self, dataingestionartifact: DataIngestionArtifact):
        try:
            logging.info("Initiate Data Validation")
            # Create DataValidationConfig using the pipeline config
            datavalidationconfig = DataValidationConfig(training_pipeline_config=self.trainingpipelineconfig)
            # Create DataValidation object and start validation
            data_validation = DataValidation(dataingestionartifact, datavalidationconfig)
            datavalidationartifact = data_validation.initiate_data_validation()
            print(datavalidationartifact)
            logging.info("Data Validation Completed")
            return datavalidationartifact
        
        except Exception as e:
            raise PhishnetException(e, sys)
        

    def start_data_transformation(self, datavalidationartifact: DataValidationArtifact):
        try:
            # Create DataTransformationConfig using the pipeline config
            datatransformationconfig = DataTransformationConfig(training_pipeline_config=self.trainingpipelineconfig)
            # Create DataTransformation object and start transformation
            data_transformation = DataTransformation(
                data_validation_artifact=datavalidationartifact,
                data_transformation_config=datatransformationconfig
            )
            datatransformationartifact = data_transformation.initiate_data_transformation()
            return datatransformationartifact
        
        except Exception as e:
            raise PhishnetException(e, sys)
        
        
    def start_model_trainer(self, datatransformationartifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            # Create ModelTrainerConfig using the pipeline config
            self.modeltrainerconfig = ModelTrainerConfig(
                training_pipeline_config=self.trainingpipelineconfig
            )

            # Create ModelTrainer object and start model training
            model_trainer = ModelTrainer(
                data_transformation_artifact=datatransformationartifact,
                model_trainer_config=self.modeltrainerconfig,
            )

            modeltrainerartifact = model_trainer.initiate_model_trainer()

            return modeltrainerartifact

        except Exception as e:
            raise PhishnetException(e, sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(dataingestionartifact = data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(datavalidationartifact = data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(datatransformationartifact = data_transformation_artifact)

            return model_trainer_artifact
        
        except Exception as e:
            raise PhishnetException(e, sys)
