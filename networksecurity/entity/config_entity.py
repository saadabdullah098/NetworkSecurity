from datetime import datetime
import os
from networksecurity.constants import training_pipeline
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier


#Testing import of constants
print(training_pipeline.ARTIFACT_DIR)
print(training_pipeline.DATA_INGESTION_DATABASE_NAME)

class TrainingPipelineConfig():
    def __init__(self, timestamp=datetime.now()):
        '''
            Initializes the pipeline name and full timestamped artifacts directory.
            
            pipeline_name: The name of the training pipeline (imported from training_pipeline).
            artifact_name: The base directory name where artifacts are stored (imported from training_pipeline).
            artifact_dir: Full path to the timestamped artifact directory where pipeline outputs will be saved.

            #Output path: Artifacts/'%m_%d_%Y_%H_%M_%S'
        '''
        timestamp = timestamp.strftime('%m_%d_%Y_%H_%M_%S')
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name,timestamp)
        self.model_dir=os.path.join("final_model")
        self.timestamp: str = timestamp



class DataIngestionConfig():
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        '''
            Initializes directories, file paths, and variables from saved constants.
            
            #Output paths: Artifacts/'%m_%d_%Y_%H_%M_%S'/data_ingestion/{feature_store or ingested}/file_name

        '''
        #Setting paths to directories
        self.data_ingestion_dir:str = os.path.join(
            training_pipeline_config.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path: str = os.path.join(
                self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, training_pipeline.FILE_NAME
            )
        self.training_file_path: str = os.path.join(
                self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME
            )
        self.testing_file_path: str = os.path.join(
                self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILE_NAME
            )
        
        #Setting train_test split
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        
        #Setting MongoDB database and collection names
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME

class DataValidationConfig():
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TEST_FILE_NAME)
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        )

class DataTransformationConfig:
     def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.transformed_train_file_path: str = os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.DATA_TRANSFORMATION_TRAIN_FILE_PATH)
        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir,  training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.DATA_TRANSFORMATION_TEST_FILE_PATH)
        self.transformed_object_file_path: str = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            training_pipeline.PREPROCESSING_OBJECT_FILE_NAME,)
        
class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.MODEL_TRAINER_DIR_NAME)
        self.trained_model_file_path: str = os.path.join(
            self.model_trainer_dir, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR, 
            training_pipeline.MODEL_FILE_NAME
        )
        self.expected_accuracy: float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold = training_pipeline.MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD
        #Lazy model creation = only instantized when variable is called avoiding unnecessary memory usage
        self.models = {
                    "Random Forest": lambda: RandomForestClassifier(verbose=1),
                    "Decision Tree": lambda: DecisionTreeClassifier(),
                    "Gradient Boosting": lambda: GradientBoostingClassifier(verbose=1),
                    "Logistic Regression": lambda: LogisticRegression(verbose=1),
                    "AdaBoost": lambda: AdaBoostClassifier(),
                }
        self.param_grid={
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

                                                