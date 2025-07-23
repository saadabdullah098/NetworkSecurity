import os
import sys
import numpy as np
import pandas as pd
import pymongo
from dotenv import load_dotenv
import certifi

from sklearn.model_selection import train_test_split
from networksecurity.logging_exception.exception import CustomException
from networksecurity.logging_exception.logger import logging

#Import configuration for data ingestion config
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

#Load env variables
load_dotenv()
MONGO_DB_URL=os.getenv('MONGO_DB_URL')

class DataIngestion():
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        #self.data_ingestion_config becomes an instance of DataIngestionConfig class
        try:
            self.data_ingestion_config = data_ingestion_config
        
        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err

    def export_collection_as_df(self):
        '''
            Reads a collection from MongoDB and converts to cleaned dataframe
        '''
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=certifi.where())
            logging.info('Sucessfully connected to MongoDB')
            collection = self.mongo_client[database_name][collection_name]

            #Read collection from MongoDB and drop _id column
            df = pd.DataFrame(collection.find())
            df.drop(columns='_id', inplace=True, errors='ignore')
            df.replace('na', np.nan, inplace=True)
            logging.info('MongoDB collection converted to dataframe')
            
            return df

        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err
    
    def export_data_to_feature_store(self, dataframe: pd.DataFrame):
        '''
            Reads raw data and saves in Artiface/feature_store folder
        '''
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path #get full file path
            
            dir_path = os.path.dirname(feature_store_file_path) #get the dir name
            os.makedirs(dir_path,exist_ok=True) #create the dir 

            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            logging.info('Raw data stored in Artiface/feature_store folder')
        
        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err
    
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        '''
            Reads raw data and splits into training and test sets and saves in Artiface/ingested folder
        '''
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")
            
            #Create directory
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info('Train Test split data stored in Artifacts/ingested folder')
            
        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err
    
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        '''
            Converts MongoDB as df then saves raw data in feature_store and train, test data in ingested.
            Returns the file paths to training and test data
        '''
        try:
            logging.info('Initiating data ingestion')
            #Call the function that returns the MongoDB as df then save raw data in feature_store
            dataframe = self.export_collection_as_df()
            self.export_data_to_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            
            logging.info('Data ingestion completed and artifact generated!')
            return data_ingestion_artifact

        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err