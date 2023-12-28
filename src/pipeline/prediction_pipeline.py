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
    def __init__(self,
                Country:str,
                Shipment_Mode:str,
                Qauntity_of_pack:int,
                Pack_Price:float,
                Weight_Kg:int,
                Product_Insurance_USD:float):
        
        self.Country=Country
        self.Shipment_Mode=Shipment_Mode
        self.Qauntity_of_pack=Qauntity_of_pack
        self.Pack_Price=Pack_Price
        self.Weight_Kg=Weight_Kg
        self.Product_Insurance_USD=Product_Insurance_USD

    def get_data_as_dataframe(self):
        try:
            Custome_data_input_dict= {
                'Country':[self.Country],
                'Shipment_Mode':[self.Shipment_Mode],
                'Quantity_of_pack':[self.Qauntity_of_pack],
                'Pack_Price':[self.Pack_Price],
                'Weight_Kg':[self.Weight_Kg],
                'Product_Insurance_USD':[self.Product_Insurance_USD],
             }
            df = pd.DataFrame(Custome_data_input_dict)
            logging.info('Data Frame Gathered')
            return df
        except Exception as e:
            logging.info("Exception occured in prediction pipeline")
            raise CustomData(e,sys)
