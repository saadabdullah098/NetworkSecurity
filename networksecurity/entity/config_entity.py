from datetime import datetime
import os
from networksecurity.constants import training_pipeline

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