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
            models = self.model_trainer_config.models
            param_grid = self.model_trainer_config.param_grid
            model_report, best_model = ml_utils.evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test,
                                                         models=models,param=param_grid)
            
            # Get best model name and score from the report
            best_model_name = max(model_report, key=model_report.get)
            best_model_score = model_report[best_model_name]
            logging.info(f'Best Model: {best_model_name}, Score: {best_model_score}')
            
            logging.info('Generating classification metric artifact using best model.')
            y_train_pred = best_model.predict(X_train)
            classification_train_metric=ml_utils.get_classification_score(y_true=y_train, y_pred=y_train_pred)

            y_test_pred = best_model.predict(X_test)
            classification_test_metric=ml_utils.get_classification_score(y_true=y_test, y_pred=y_test_pred)
            
            logging.info('Saving model object containing preprocessor and model with function to make future predictions.')
            # Create directory to save best model and save NetworkModel obj containing preprocessor and model which can also be used to predict
            os.makedirs(os.path.dirname(self.model_trainer_config.trained_model_file_path),exist_ok=True)

            preprocessor = main_utils.load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            Network_Model=ml_utils.NetworkModel(preprocessor=preprocessor,model=best_model)
            main_utils.save_object(self.model_trainer_config.trained_model_file_path, obj=Network_Model)
            logging.info('Final model object saved.')
            

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                train_metric_artifact=classification_train_metric,
                                test_metric_artifact=classification_test_metric
                                )
            
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        
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
            model_trainer_artifact = self.train_and_evaluate_model(X_train, y_train, X_test, y_test)

            logging.info('Models trained and evaluated, best model chosen, and artifact generated.')
            return model_trainer_artifact


        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err