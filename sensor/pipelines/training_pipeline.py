from sensor.logger import logging
from sensor.exception import SensorException
from sensor.utils import get_collection_as_dataframe
import sys, os
from sensor.entity import config_entity
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_pusher import ModelPusher


def start_training_pipeline():
    try:
        print("Step 1: Initializing TrainingPipelineConfig")
        training_pipeline_config = config_entity.TrainingPipelineConfig()

        # data ingestion
        print("Step 2: Data Ingestion")
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print("Data Ingestion Complete")
        
        # data validation
        print("Step 3: Data Validation")
        data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config,
                        data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact = data_validation.initiate_data_validation()
        print("Data Validation Complete")

        # data transformation
        print("Step 4: Data Transformation")
        data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config, 
        data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print("Data Transformation Complete")
        
        # model trainer
        print("Step 5: Model Trainer")
        model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        print("Model Trainer Complete")

        # model evaluation
        print("Step 6: Model Evaluation")
        model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
        model_eval  = ModelEvaluation(model_eval_config=model_eval_config,
        data_ingestion_artifact=data_ingestion_artifact,
        data_transformation_artifact=data_transformation_artifact,
        model_trainer_artifact=model_trainer_artifact)
        model_eval_artifact = model_eval.initiate_model_evaluation()
        print("Model Evaluation Complete")

        # model pusher
        print("Step 7: Model Pusher")
        model_pusher_config = config_entity.ModelPusherConfig(training_pipeline_config)
        model_pusher = ModelPusher(model_pusher_config=model_pusher_config, 
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_artifact=model_trainer_artifact)
        model_pusher_artifact = model_pusher.initiate_model_pusher()
        print("Model Pusher Complete")
    except Exception as e:
        print(f"Exception occurred: {e}")
        raise SensorException(e, sys)


if __name__ == "__main__":
    print("Starting training pipeline...")
    start_training_pipeline()
