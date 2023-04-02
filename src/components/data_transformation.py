import sys
import dataclasses import dataclass

import numpys as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearning.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

class DataTransformationConfig:               #change
    preprocessor_obj_file_path=os.pathg.join('artifacts',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
    
       ''' This Function is responsible for data transformation'''

       try:

            numerical_columns =[" ", " "]
            categorical_columns =[" "," "]
            num_pipeline = Pipeline(
            steps=[
            ("imputer",SimpleImputer(strategy="median")),
            ("scaler",StandardScaler())
            ]
          )
        cat_pipeline = Pipeline(
            steps =[
            ("imputer",SimpleImputer(strategy="most_frequent")),
            ("one_hot_encoder",OneHotEncoder()),
            ("scaler",StandardScaler())
            ]
          )
        
        logging.info("Numerical /Categorical completed")

        preprocessor = ColumnTransformer(
            [
            ("num_pipeline",num_pipeline,numerical_columns),
            ("cat_pipeline",cat_pipeline,categorical_columns)
            ]
          )
        return preprocessor
        
      except Exception as e:
        raise CustomException(e,sys)
    
    def initiate_data_transformation(self,train_path,test_path):

        try:
            pass
        except:
            pass