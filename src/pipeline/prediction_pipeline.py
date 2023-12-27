import os
import sys
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object
import pandas as pd

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        try:
            preprocessor_ath=os.path.join('artifact','preprocessor.pkl')
            model_path=os.path.join('artifact','model.pkl')

            
            
                   
        except Exception as e:
            logging.info('Exception occured in Prediction Pipeline')
            raise CustomException(e,sys)


