import os
import sys

from phishnet.entity.config_entity import ModelTrainerConfig
from phishnet.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact

from phishnet.utils.main_utils.utils import save_object, load_object
from phishnet.utils.main_utils.utils import load_numpy_array_data, evaluate_models

from phishnet.utils.ml_utils.metric.classification_metric import get_classification_score
from phishnet.utils.ml_utils.model.estimator import PhishnetModel

from phishnet.exception.exception import PhishnetException
from phishnet.logging.logger import logging

# Importing ML models
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.metrics import r2_score

class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise PhishnetException(e, sys)
        
    def train_model(self, train_features, train_labels, test_features, test_labels):
        """
        Train multiple models, evaluate them, and select the best model based on performance.
        """
        try:
            # Define models and their hyperparameters
            models = {
                "Logistic Regression": LogisticRegression(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Random Forest": RandomForestClassifier(verbose=1),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "AdaBoost": AdaBoostClassifier()
            }

            # Hyperparameter tuning for each model
            params = {
                "Decision Tree": {
                    'criterion': ['gini', 'entropy', 'log_loss'],
                },
                "Random Forest": {
                    'n_estimators': [8, 16, 32, 128, 256]
                },
                "Gradient Boosting": {
                    'learning_rate': [0.1, 0.01, 0.05, 0.001],
                    'subsample': [0.6, 0.7, 0.75, 0.85, 0.9],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Logistic Regression": {},
                "AdaBoost": {
                    'learning_rate': [0.1, 0.01, 0.001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                }
            }

            # Evaluate models using the utility function
            model_report: dict = evaluate_models(
                x_train=train_features,
                y_train=train_labels,
                x_test=test_features,
                y_test=test_labels,
                models=models,
                param=params
            )

            # Get the best model based on test score
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]

            # Train the best model and evaluate on train and test data
            best_model.fit(train_features, train_labels)
            train_predictions = best_model.predict(train_features)
            test_predictions = best_model.predict(test_features)

            # Calculate classification metrics
            train_metrics = get_classification_score(y_true=train_labels, y_pred=train_predictions)
            test_metrics = get_classification_score(y_true=test_labels, y_pred=test_predictions)

            # Save the best model and preprocessor
            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            phishnet_model = PhishnetModel(preprocessor=preprocessor, model=best_model)

            save_object(self.model_trainer_config.trained_model_file_path, obj=phishnet_model)

            # Create and return the model trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=train_metrics,
                test_metric_artifact=test_metrics
            )
            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise PhishnetException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        """
        Load transformed data, train models, and return the best model artifact.
        """
        try:
            # Load transformed train and test data
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_data = load_numpy_array_data(train_file_path)
            test_data = load_numpy_array_data(test_file_path)

            # Separate features and labels
            train_features, train_labels = train_data[:, :-1], train_data[:, -1]
            test_features, test_labels = test_data[:, :-1], test_data[:, -1]

            # Train models and get the best model artifact
            model_trainer_artifact = self.train_model(
                train_features=train_features,
                train_labels=train_labels,
                test_features=test_features,
                test_labels=test_labels
            )

            return model_trainer_artifact

        except Exception as e:
            raise PhishnetException(e, sys)