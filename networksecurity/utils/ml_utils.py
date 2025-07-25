import sys
from networksecurity.logging_exception.exception import CustomException
from networksecurity.logging_exception.logger import logging

from networksecurity.entity.artifact_entity import ClassificationMetricArtifact

from sklearn.metrics import r2_score
from sklearn.metrics import f1_score,precision_score,recall_score
from sklearn.model_selection import GridSearchCV

def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    '''
        Evaluates a list of models based on given parameters and generates a report comparing the models.
    '''
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err
    

def get_classification_score(y_true,y_pred)->ClassificationMetricArtifact:
    '''
        Calculates f1_score, recall_score, and precision_score and returns the artifact contaiing the scores.
    '''
    try:
        model_f1_score = f1_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_precision_score=precision_score(y_true,y_pred)

        classification_metric =  ClassificationMetricArtifact(f1_score=model_f1_score,
                    precision_score=model_precision_score, 
                    recall_score=model_recall_score)
        return classification_metric
    
    except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err
    
class NetworkModel:
    '''
        Loads the preprocessor and model, and uses it to transform and make predictions on new data.
    '''
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        
        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err
    
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        
        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err