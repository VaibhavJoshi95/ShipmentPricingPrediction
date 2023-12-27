import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
import os
import sys

from dataclasses import dataclass

@dataclass
class ModelTrainerConfig:
        trained_model_file_path=os.path.join('artifact','model.pkl')

class ModelTrainer:
    def __init__(self):
          self.model_trainer_config = ModelTrainerConfig()
        
    def initiate_model_training(self,train_array,test_array):
          try:
                logging.info('Splitting Dependent and Independent Variable from train and test data')

                X_train,y_train,X_test,y_test=(
                      train_array[:,:-1],
                      train_array[:,-1],
                      test_array[:,:-1],
                      test_array[:,-1]
                )

                param_grid={
                'n_estimators': [25, 50],  
                'max_depth': [None, 10, 20, 30],  
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
                rf_regressor=RandomForestRegressor()

                grid_search = GridSearchCV(estimator=rf_regressor, param_grid=param_grid, cv=5, scoring='r2',n_jobs=1)

                grid_search.fit(X_train, y_train)

                best_rf_model = grid_search.best_estimator_

                best_model_score = best_rf_model.score(X_test, y_test)
                print(f'Best Random Forest Model Found, R2 Score: {best_model_score}')

                logging.info(f'Best Random Forest Model Found, R2 Score: {best_model_score}')

                save_object(
                      file_path=self.model_trainer_config.trained_model_file_path, 
                      obj=best_rf_model)
                


          except Exception as e:
                logging.info('EXception occured in model training')
                raise CustomException(e,sys)
          

                