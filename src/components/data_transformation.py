import os
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder,StandardScaler
from src.exception import CustomException
from src.logger import logging
import sys
from dataclasses import dataclass
from src.utils import save_object

@dataclass

class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifact','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_tranformation_config=DataTransformationConfig()

    def get_data_transformation_object(self):
        try:
            logging.info('Data Transformation initiated')

            categorical_cols=['Country', 'Shipment_Mode']
            numerical_cols=['Qauntity_of_pack', 'Pack_Price', 'Weight_kG','Product_Insurance_USD']

            Country_categories=['Rwanda', 'Vietnam', "Côte dIvoire", 'Burundi', 'Mozambique','Uganda', 'Zambia', 'Namibia', 'Congo, DRC', 'Kenya', 'Zimbabwe',
                                'Ethiopia', 'Guyana', 'Nigeria', 'Sudan', 'South Africa','Guatemala', 'Ghana', 'Haiti', 'Botswana', 'Pakistan',
                                'Dominican Republic', 'Liberia', 'Swaziland', 'Afghanistan','Cameroon', 'Malawi', 'Lesotho', 'Senegal', 'Tanzania',
                                'South Sudan', 'Libya', 'Mali', 'Angola', 'Benin', 'Guinea','Togo', 'Sierra Leone']
            
            Shipment_Mode_categories=['Air', 'Truck', 'Air Charter', 'Ocean']

            logging.info('Pipeline Initiated')

            #Numerical Pipeline

            num_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ]
            )

            #categorical Piepleine

            cat_pipeline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('encoder',OrdinalEncoder(categories=[Country_categories,Shipment_Mode_categories])),
                    ('scaler',StandardScaler())
                ]
            )

            preprocessor=ColumnTransformer([
                ('num_pipeline',num_pipeline,numerical_cols),
                ('cat_pipeline',cat_pipeline,categorical_cols)
            ])
            
            return preprocessor
            logging.info('Pipeline Completed')


        except Exception as e:
            logging.info('Exception ocured in Data tRansformation method')
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            #reading Train and Test data
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            logging.info("Read Train and Test data completed")
            logging.info(f'Train Dataframe Head:\n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head:\n{test_df.head().to_string()}')
            logging.info('Obtaining Preprocessing object')

            preprocessing_obj=self.get_data_transformation_object()

            target_column_name='Freight_Cost_USD'
            drop_columns=[target_column_name]

            input_feature_train_df=train_df.drop(columns=drop_columns,axis=1)
            target_feature_train_df=train_df[target_column_name]
            input_feature_test_df=test_df.drop(columns=target_column_name,axis=1)
            target_feature_test_df=test_df[target_column_name]

            ## Transorming using preprocessor obj

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            logging.info("Applying preprocessing object on training and testing datasets")

            train_arr=np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            save_object(file_path=self.data_tranformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj)
            logging.info('Preprocessor pickle file saved')

            return(
                train_arr,
                test_arr,
                self.data_tranformation_config.preprocessor_obj_file_path
            )       
            
           


        except Exception as e:
            logging.info('Excpetion occured in the data initiate_datatransformation')
            raise CustomException(e,sys)