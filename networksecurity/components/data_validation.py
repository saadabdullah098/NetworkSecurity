import os, sys
import pandas as pd
from scipy.stats import ks_2samp
from networksecurity.logging_exception.exception import CustomException
from networksecurity.logging_exception.logger import logging

#Import configuration for data validation config
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils import main_utils

class DataValidation():
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        #initializing artifacts, config, and schema file  
        try:
            logging.info('Initializing validation artifacts, config, and schema files')
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = main_utils.read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err

    def validate_number_of_columns_and_names(self, dataframe:pd.DataFrame)->bool:
        '''
            Checks the number of columns and compares names of columns for match.
        '''
        try:
            expected_columns = list(self._schema_config['columns'].keys())
            df_columns = list(dataframe.columns)
            logging.info(f'Expected number of columns: {len(expected_columns)}')
            logging.info(f'Actual number of columns: {len(df_columns)}')
            
            #Check lengths of columns
            if len(df_columns) != len(expected_columns):
                logging.warning(f"Column count mismatch. Expected {len(expected_columns)}, got {len(df_columns)}")
                return False

            #Check column names
            if set(df_columns) != set(expected_columns):
                missing = set(expected_columns) - set(df_columns)
                extra = set(df_columns) - set(expected_columns)
                logging.warning(f"Missing columns: {missing}" if missing else "")
                logging.warning(f"Unexpected columns: {extra}" if extra else "")
                return False

            return True
        
        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err


    def detect_dataset_drift(self, base_df, current_df, threshold=0.05)->bool:
        '''
            Checks distribution between columns in two dataframes and determines if there is drift in the distributions
            using Kolmogorov-Smirnov non-parametric test.
        '''
        try:
            status = True
            report = {}
            #Compare distributions column by column
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2) #compare distribution of 2 samples
                
                if is_same_dist.pvalue < threshold:
                    is_found = True    # Drift detected
                    status = False     # Overall status becomes False
                    logging.warning(f'Drift detected in {column} column')
                else:
                    is_found = False   # No drift detected
                report.update({
                        column:{
                            'p-value':float(is_same_dist.pvalue),
                            'drift_status':is_found
                        }
                    })
            
            #Save report in YAML file
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            main_utils.write_yaml_file(file_path=drift_report_file_path, content=report)
            logging.info('Data drift report generated.')
            return status
        
        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err
    
    def initialize_data_validation(self)->DataValidationArtifact:
        logging.info('Initiating data validation')
        try:
            #Read data
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            train_df = main_utils.read_csv_data(train_file_path)
            test_df = main_utils.read_csv_data(test_file_path)
            logging.info('Train and test data read and stored.')

            #Validate number of columns
            status_train=self.validate_number_of_columns_and_names(dataframe=train_df)
            if not status_train:
                logging.warning("Train dataframe does not contain all required columns.")
            
            status_test=self.validate_number_of_columns_and_names(dataframe=test_df)
            if not status_test:
                logging.warning("Test dataframe does not contain all required columns.")
            
            logging.info(f'Train Data Column Validation Status: {status_train}')
            logging.info(f'Test Data Column Validation Status: {status_test}')
            logging.info('Column validation process complete.')
            
            #Check data drift. Comparing train and test here but can also compare new data as it comes in.
            status_drift = self.detect_dataset_drift(base_df=train_df, current_df=test_df) 
            logging.info(f'Data Drift Validation Status: {status_drift}')
            
            #Give final status of validation
            status = status_train and status_test and status_drift
            logging.info(f'Final Validation Status: {status}')

            #Save data to directory based on status
            os.makedirs(self.data_validation_config.valid_data_dir, exist_ok=True)
            os.makedirs(self.data_validation_config.invalid_data_dir, exist_ok=True)
            if status == True:
                train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
                test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)
            else:
                train_df.to_csv(self.data_validation_config.invalid_train_file_path, index=False, header=True)
                test_df.to_csv(self.data_validation_config.invalid_test_file_path, index=False, header=True)

            #Generate validation artifact
            data_validation_artifact = DataValidationArtifact(
                validation_status = status,
                valid_train_file_path = self.data_validation_config.valid_train_file_path,
                valid_test_file_path = self.data_validation_config.valid_test_file_path,
                invalid_train_file_path = self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path = self.data_validation_config.invalid_test_file_path,
                drift_report_file_path = self.data_validation_config.drift_report_file_path
            )
            logging.info('Data validation completed and artifact generated!')
            logging.info(data_validation_artifact)
            return data_validation_artifact
            
        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err
        
