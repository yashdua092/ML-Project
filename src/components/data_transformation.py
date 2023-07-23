import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer # used to create a pipeline for transfroming a column
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.logger import logging
from src.exception import CustomException
from src.utils import save_object # for saving preprocessor obj in pkl file

@dataclass
class DataTransformConfig: # any inputs required for data transformation
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformatiom:
    def __init__(self):
        self.data_transformation_config = DataTransformConfig()

    def get_data_transform_object(self):
        try:
            numerical_columns = [
                'writing_score',
                'reading_score'
            ]
            categorical_columns = [
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]

            num_pipeline = Pipeline( # pipeline for numerical features transformation
                steps = [
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            cat_pipeline = Pipeline( # pipeline for categorical features transformation
                steps = [
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            logging.info(f"categorical columns: {categorical_columns}")
            logging.info(f"numerical columns: {numerical_columns}")

            preprocessor = ColumnTransformer( # pipeline for a column transformation
                [
                    ("num_pipeline", num_pipeline, numerical_columns), # name, pipeline, features
                    ("cat_pipeline", cat_pipeline, categorical_columns),

                ]
            )

            return preprocessor # basically returning everything.

        except Exception as e:
            raise CustomException(e, sys)
        
    
    def initiate_data_transformation(self, train_path, test_path):
        # we already have the data in specific folder thanks to ingestion.py

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("reading of data completed")
            logging.info("obtaining preprocessing object") # that contains all the pipeline for transformation

            preprocessing_obj = self.get_data_transform_object()

            target_column_name = "math_score"

            # creating the data to pass to preprocessing obj
            input_features_train_df = train_df.drop(columns = [target_column_name], axis=1)
            target_features_train_df = train_df[target_column_name]
            
            input_features_test_df = test_df.drop(columns = [target_column_name], axis=1)
            target_features_test_df = test_df[target_column_name]

            logging.info(
                f"Applying processing object on training and testing dataframe."
            )

            input_feature_train_arr = preprocessing_obj.fit_transform(input_features_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_features_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_features_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_features_test_df)
            ]

            logging.info("saved preprocessing object")

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)
