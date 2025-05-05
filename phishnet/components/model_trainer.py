import os
import sys

from phishnet.entity.config_entity import ModelTrainerConfig
from phishnet.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact

from phishnet.utils.main_utils.utils import save_object, load_object
from phishnet.utils.main_utils.utils import load_numpy_array_data

from phishnet.utils.ml_utils.metric.classification_metric import get_classification_score
from phishnet.utils.ml_utils.model.estimator import PhishnetModel

from phishnet.exception.exception import PhishnetException

class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise PhishnetException(e, sys)
        
    def train_model(self, x_train, y_train):
        # TODO 
        return 0


    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )
            model = self.train_model(x_train, y_train)

        except Exception as e:
            raise PhishnetException(e, sys)