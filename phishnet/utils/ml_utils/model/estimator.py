import os
import sys

from phishnet.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME
from phishnet.exception.exception import PhishnetException
from phishnet.logging.logger import logging

class PhishnetModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model

        except Exception as e:
            raise PhishnetException(e, sys)
        
    def predict(self, x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            
            return y_hat
        
        except Exception as e:
            raise PhishnetException(e, sys)