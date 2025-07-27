import sys
from networksecurity.logging_exception.exception import CustomException
from networksecurity.logging_exception.logger import logging

from networksecurity.entity.artifact_entity import ClassificationMetricArtifact

from sklearn.metrics import r2_score
from sklearn.metrics import f1_score,precision_score,recall_score
from sklearn.model_selection import GridSearchCV


def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    '''
        Evaluates multiple models with given hyperparameters and returns:
        - a dictionary of test scores
        - the best performing trained model
    '''
    try:
        report = {}
        best_model = None
        best_model_name = None
        best_score = float('-inf')  # Initialize to negative infinity

        for model_name, model_fn in models.items():
            model = model_fn()
            param_grid = param.get(model_name, {})

            if param_grid:
                gs = GridSearchCV(model, param_grid, cv=3, n_jobs=-1)
                gs.fit(X_train, y_train)
                model = gs.best_estimator_
            else:
                model.fit(X_train, y_train)

            y_test_pred = model.predict(X_test)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_model_score

            # Keep track of the best model
            if test_model_score > best_score:
                best_score = test_model_score
                best_model = model
                best_model_name = model_name

        return report, best_model, best_model_name, best_score

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
        

