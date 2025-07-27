import os, sys
from dotenv import load_dotenv
from networksecurity.logging_exception.exception import CustomException
from networksecurity.logging_exception.logger import logging
from networksecurity.entity.config_entity import TrainingPipelineConfig, ModelTrainerConfig

import mlflow
import mlflow.sklearn
import dagshub
import joblib


#Load credentials and uri for mlflow and dagshub
load_dotenv()
mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
mlflow_username = os.getenv("MLFLOW_TRACKING_USERNAME")
mlflow_password = os.getenv("MLFLOW_TRACKING_PASSWORD")

os.environ["MLFLOW_TRACKING_URI"] = mlflow_tracking_uri
os.environ["MLFLOW_TRACKING_USERNAME"] = mlflow_username
os.environ["MLFLOW_TRACKING_PASSWORD"] = mlflow_password


def track_mlflow(best_model, classification_metric):
        '''
        Tracks machine learning lifecycle using MLflow including metrics and models
        '''
        try:
            with mlflow.start_run(run_name="model_tracking"):

                # Optional: Log parameters or tags (for better organization)
                mlflow.set_tags({"model_type": type(best_model).__name__})

                # Log metrics
                mlflow.log_metric("f1_score", classification_metric.f1_score)
                mlflow.log_metric("precision", classification_metric.precision_score)
                mlflow.log_metric("recall_score", classification_metric.recall_score)

                # Save model locally
                training_pipeline_config = TrainingPipelineConfig()
                model_trainer_config = ModelTrainerConfig(training_pipeline_config)
                model_path = f"{model_trainer_config.model_trainer_dir}/mlflow_artifact/best_model.pkl"
                os.makedirs(os.path.dirname(model_path), exist_ok=True)
                joblib.dump(best_model, model_path)

                # Log as artifact instead of using model registry
                mlflow.log_artifact(model_path, artifact_path="model")

        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err