import sys
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.logging_exception.exception import CustomException
from networksecurity.logging_exception.logger import logging

from networksecurity.constants.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from networksecurity.utils import main_utils

class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            logging.info('Initializing transformation artifacts, config, and schema files')
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err

    def get_data_transformer_object(cls)->Pipeline:
        '''
            Initializes a KNNImputer object with parameters defined in training_pipeline constants 
            and returns a Pipeline object with the KNNImputer object as the first step.

            This is a method of the class rather than of an instance.
        '''
        try:
            logging.info(f'Initializing KNNImputer with parameters: {DATA_TRANSFORMATION_IMPUTER_PARAMS}')
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)

            processor:Pipeline = Pipeline([('imputer',imputer)])
            return processor

        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err

    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info('Initiating data transformation.')
        try:
            train_df = main_utils.read_csv_data(self.data_validation_artifact.valid_train_file_path)
            test_df = main_utils.read_csv_data(self.data_validation_artifact.valid_test_file_path)

            logging.info('Separating input and target features')
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            logging.info('Replacing -1 with 0s in target feature columns (will contain 0s and 1s)')
            target_feature_train_df = target_feature_train_df.replace(-1,0)
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            logging.info('Imputing missing values with KNNImputer preprocessor')
            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            logging.info('Combining transformed inputs with target columns')
            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df) ]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df) ]

            logging.info('Saving numpy array data and preprocessor object')
            main_utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path, array=train_arr)
            main_utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path, array=test_arr)
            main_utils.save_object(file_path=self.data_transformation_config.transformed_object_file_path, obj=preprocessor_object)

            logging.info('Preparing transformation artifacts')
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )

            logging.info('Data transformation complete and artifacts generated!')
            logging.info(data_transformation_artifact)
            return data_transformation_artifact


        except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err