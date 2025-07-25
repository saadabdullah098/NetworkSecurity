import sys, os
from networksecurity.logging_exception.exception import CustomException
from networksecurity.logging_exception.logger import logging

from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.utils import main_utils, ml_utils

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)
from sklearn.metrics import r2_score


class ModelTrainer:
    def __init__(self, data_transformation_artifact:DataTransformationArtifact, model_trainer_config:ModelTrainerConfig):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err
    
    def train_and_evaluate_model(self, X_train, y_train, X_test, y_test):
        try:
            models = {
                    "Random Forest": RandomForestClassifier(verbose=1),
                    "Decision Tree": DecisionTreeClassifier(),
                    "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                    "Logistic Regression": LogisticRegression(verbose=1),
                    "AdaBoost": AdaBoostClassifier(),
                }
            
            params={
                "Decision Tree": {
                    'criterion':['gini', 'entropy', 'log_loss'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['gini', 'entropy', 'log_loss'],
                    
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['log_loss', 'exponential'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Logistic Regression":{},
                "AdaBoost":{
                    'learning_rate':[.1,.01,.001],
                    'n_estimators': [8,16,32,64,128,256]
                }
            }
        
        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err



    def initiate_model_trainer(self)->ModelTrainerArtifact:
        logging.info('Initiating model trainer.')
        try:
            logging.info('Loading train and test arrays.')
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = main_utils.load_numpy_array_data(train_file_path)
            test_arr = main_utils.load_numpy_array_data(test_file_path)

            X_train, y_train, X_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            
            logging.info('Training and evaluating models')
            self.train_and_evaluate_model(X_train, y_train)


        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err