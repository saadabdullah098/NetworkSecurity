import os
import sys
import certifi
from dotenv import load_dotenv

import pymongo
import pandas as pd
import numpy as np 

from networksecurity.logging_exception.exception import CustomException
from networksecurity.logging_exception.logger import logging

#Initialize env variables 
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

#Store path to a trusted root certificate bundle (a .pem file)
ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err
        
    def csv_to_json(self, file_path: str):
        '''
            Reads a CSV file and returns it as a list of dictionaries,
            where each dictionary represents a row.
        '''
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = data.to_dict(orient="records") #orient="records" converts each row into a dictionary
            return records

        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err
        
    def insert_data_to_mongoDB(self, records, database, collection):
        '''
            Inserts a list of records into a specified MongoDB collection.

            Parameters
            records : A list of dictionaries where each dictionary represents a document to insert.
            database : The name of the MongoDB database where the data will be inserted.
            collection : The name of the collection within the database where the records will be inserted.
        '''
        try:
            self.records = records
            self.database = database
            self.collection = collection
            
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=certifi.where())
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)

            return len(self.records)
        
        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err
        

if __name__ == '__main__':
    FILE_PATH = 'Network_Data/phisingData.csv'
    DATABASE = 'NetworkSecurityData'
    COLLECTION = 'NetworkData'

    networkobj = NetworkDataExtract()

    records = networkobj.csv_to_json(file_path=FILE_PATH)

    no_of_records = networkobj.insert_data_to_mongoDB(records=records, database=DATABASE, collection=COLLECTION)
    
    print(f'Number of records sucesfully inserted into {DATABASE} database: {no_of_records}')
