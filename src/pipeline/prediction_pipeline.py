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
            preprocessor_path=os.path.join('artifact','preprocessor.pkl')
            model_path=os.path.join('artifact','model.pkl')

            preprocessor=load_object(preprocessor_path)
            model=load_object(model_path)

            data_scaled=preprocessor.transform(features)

            pred=model.predict(data_scaled)
            return pred            
            
                   
        except Exception as e:
            logging.info('Exception occured in Prediction Pipeline')
            raise CustomException(e,sys)
        
class CustomData:
    def __int__(self,Qauntity_of_pack:int,Pack Price:float, Weight(Kilograms):float,Product_Insurance_USD:float,
                Country:str,Shipment Mode:str):


