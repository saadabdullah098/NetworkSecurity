import os, sys
import yaml
import numpy as np
import pandas as pd
import dill, pickle
from networksecurity.logging_exception.exception import CustomException
from networksecurity.logging_exception.logger import logging

def read_csv_data(file_path)->pd.DataFrame:
    #Reads csv file from file path
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        custom_err = CustomException(e, sys)
        logging.error(custom_err)
        raise custom_err

def read_yaml_file(file_path: str)->dict:
    #Reads and loads a yaml file as a dictionary
    try:
        with open(file_path, 'rb') as yaml_file:
             return yaml.safe_load(yaml_file)
        
    except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err

def write_yaml_file(file_path: str, content:object, replace: bool = False)->None:
    '''
        Creates folder and file in file path and writes the content. 
        Removes file at file path if replace set to True.
    '''
    try:
        if replace:
             if os.path.exists(file_path):
                  os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
             yaml.dump(content, file) 
        
    except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err

def save_numpy_array_data(file_path: str, array: np.array):
    '''
        Creates directory for file and saves numpy array data to file.
    '''
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
             np.save(file_obj, array)
        
    except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err
    
def save_object(file_path:str, obj:object)->None:
    '''
        Creates directory for file and saves object files in .pkl format.
    '''
    try:
         os.makedirs(os.path.dirname(file_path), exist_ok=True)
         with open (file_path, 'wb') as file_obj:
              pickle.dump(obj, file_obj)
        
    except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err
     