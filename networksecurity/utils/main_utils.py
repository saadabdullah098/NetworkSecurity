import os, sys
import yaml
import numpy as np
import dill, pickle
from networksecurity.logging_exception.exception import CustomException
from networksecurity.logging_exception.logger import logging


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