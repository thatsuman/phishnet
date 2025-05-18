import os
import sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from phishnet.constant.training_pipeline import TARGET_COLUMN
from phishnet.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from phishnet.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact

from phishnet.entity.config_entity import DataTransformationConfig
from phishnet.exception.exception import PhishnetException
from phishnet.logging.logger import logging
from phishnet.utils.main_utils.utils import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        # Initialize DataTransformation with validation artifact and transformation config
        try:
            self.data_validation_artifact:DataValidationArtifact = data_validation_artifact
            self.data_transformation_config:DataTransformationConfig = data_transformation_config

        except Exception as e:
            raise PhishnetException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        # Read a CSV file into a pandas DataFrame
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise PhishnetException(e, sys)

    def get_data_transformer_object(cls) -> Pipeline:
        """
        It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file and returns a Pipeline object with the KNNImputer object as the first step.

        Args:
            cls: DataTransformation
        
        Returns:
            A Pipeline object
        """
        logging.info(
            "Entered get_data_transformer_object method of Transformation class"
        )
        try:
            # Initialize KNNImputer with parameters from config
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")

            # Create a pipeline with the imputer
            processor:Pipeline = Pipeline([("imputer",imputer)])

            return processor
        
        except Exception as e:
            raise PhishnetException(e, sys)



    def initiate_data_transformation(self) -> DataTransformationArtifact:
        # Main method to perform data transformation and save artifacts
        logging.info("Entered initiate_data_transformation method of DataTransformation class")

        try:
            logging.info("Starting data transformation")    
            # Read validated train and test data
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            # Training dataframe: separate input features and target
            input_feature_train_df = train_df.drop(columns = [TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)

            # Testing dataframe: separate input features and target
            input_feature_test_df = test_df.drop(columns = [TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            # Get the data transformer pipeline and fit on training input features
            prepocessor = self.get_data_transformer_object()
            prepocessor_object = prepocessor.fit(input_feature_train_df)
            # Transform both train and test input features
            transformed_input_train_feature = prepocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = prepocessor_object.transform(input_feature_test_df)

            # Concatenate transformed features with target arrays
            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            # Save transformed numpy arrays and preprocessor object
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, prepocessor_object)


            save_object("final_model/preprocessor.pkl",prepocessor_object)
            
            # Preparing artifacts for downstream pipeline steps
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifact
        
        except Exception as e:
            raise PhishnetException(e, sys)