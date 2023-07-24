import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformatiom
from src.components.data_transformation import DataTransformConfig
from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

# decorators wrap a function, modifying its behavior.
# let the function be 'f', pass a reference to another function
# check if certain conditions met or how you wanna use this 'f' function
# then call this function. That's how decorators help to add extra functionality or boundations

# ************************************************************************************************************************************************

# def my_decorator(func):
#     def wrapper():
#         print("Something is happening before the function is called.")
#         func()
#         print("Something is happening after the function is called.")
#     return wrapper

# @my_decorator
# def say_whee():
#     print("Whee!")

# So, @my_decorator is just an easier way of saying:
# say_whee = my_decorator(say_whee). It’s how you apply a decorator to a function.

# SO,

# f = my_decorator(f), passing 'f' reference to decorator. basically 'f' decorator se hokr execute hoga.

# ************************************************************************************************************************************************

@dataclass
class DataIngestionConfig:
    # contains path where to save raw data, train and test data
    train_data_path: str =  os.path.join('artifacts', "train.csv")
    test_data_path: str =  os.path.join('artifacts', "test.csv")
    raw_data_path: str =  os.path.join('artifacts', "data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        logging.info("Inside the data ingestion method or component")
        try:
            # read the whole dataset and save it into data.csv
            # divide it into train set and save it into train.csv
            # and finally divide into test set and save into test.csv

            df = pd.read_csv('notebook\data\stud.csv')
            logging.info("read the dataset as dataframe")
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok = True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True) # will get the raw csv in this path

            logging.info("performing train test split")

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True) # will get the train csv in this path
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True) # will get the test csv in this path
            
            logging.info("ingestion is completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformatiom()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)

    modelTrainer = ModelTrainer()
    print(modelTrainer.initiate_model_trainer(train_arr, test_arr))