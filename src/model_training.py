import os
import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score,precision_score,recall_score,roc_auc_score
from src.logger import get_logger
from src.custom_exception import CustomException
import mlflow
import mlflow.sklearn

logger = get_logger(__name__)

class ModelTraining:
    def __init__(self,processed_data_path = "artifacts/processed"):
        self.processed_data_path = processed_data_path
        self.model_output_path = "artifacts/model"
        
        os.makedirs(self.model_output_path, exist_ok=True)
        logger.info("ModelTraining initialized with processed data path: %s and model output path: %s", self.processed_data_path, self.model_output_path)
    def load_data(self):
        try:
            self.X_train = joblib.load(os.path.join(self.processed_data_path, "X_train.pkl"))
            self.y_train = joblib.load(os.path.join(self.processed_data_path, "y_train.pkl"))
            self.X_test = joblib.load(os.path.join(self.processed_data_path, "X_test.pkl"))
            self.y_test = joblib.load(os.path.join(self.processed_data_path, "y_test.pkl"))
            logger.info("Data loaded successfully from %s", self.processed_data_path)
        except Exception as e:
            logger.error("Error loading data: %s", e)
            raise CustomException(f"Error loading data: {e}")
    def train_model(self):
        try:
            self.model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
            self.model.fit(self.X_train, self.y_train)
            joblib.dump(self.model, os.path.join(self.model_output_path, "model.pkl"))
            logger.info("Model trained successfully")
        except Exception as e:
            logger.error("Error training model: %s", e)
            raise CustomException(f"Error training model: {e}")
    def evaluate_model(self):
        try:
            y_pred = self.model.predict(self.X_test)
            accuracy = accuracy_score(self.y_test, y_pred)
            f1 = f1_score(self.y_test, y_pred, average='weighted')
            precision = precision_score(self.y_test, y_pred, average='weighted')
            recall = recall_score(self.y_test, y_pred, average='weighted')
            roc_auc = roc_auc_score(self.y_test, self.model.predict_proba(self.X_test)[:, 1])
            
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("f1_score", f1)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.log_metric("roc_auc", roc_auc)

            logger.info("Model evaluation metrics:")
            logger.info(f"Accuracy: {accuracy}")
            logger.info(f"F1 Score: {f1}")
            logger.info(f"Precision: {precision}")
            logger.info(f"Recall: {recall}")
            logger.info(f"ROC AUC: {roc_auc}")
        except Exception as e:
            logger.error("Error evaluating model: %s", e)
            raise CustomException(f"Error evaluating model: {e}")
    def run(self):
        try:
            self.load_data()
            self.train_model()
            self.evaluate_model()
            logger.info("Model training and evaluation completed successfully")
        except Exception as e:
            logger.error("An unexpected error occurred: %s", e)
            raise CustomException(f"An unexpected error occurred: {e}")
if __name__ == "__main__":
    with mlflow.start_run():
        model_trainer = ModelTraining()
        model_trainer.run()