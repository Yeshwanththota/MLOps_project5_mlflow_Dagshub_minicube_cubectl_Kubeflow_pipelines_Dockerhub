import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_selection import SelectKBest,chi2
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

class DataProcessing:
    def __init__(self,input_path,output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_selector = None
        self.df = None
        self.X = None
        self.Y = None
        self.selected_features = []

        os.makedirs(self.output_path, exist_ok=True)
        logger.info("DataProcessing initialized with input path: %s and output path: %s", self.input_path, self.output_path)
    def load_data(self):
        try:
            self.df = pd.read_csv(self.input_path)
            logger.info("Data loaded successfully from %s", self.input_path)
        except Exception as e:
            logger.error("Error loading data: %s", e)
            raise CustomException(f"Error loading data: {e}")
    def preprocess_data(self):
        try:
            self.df = self.df.drop(columns=['Patient_ID'])
            self.X = self.df.drop(columns=['Survival_Prediction'])
            self.Y = self.df["Survival_Prediction"]
            categorical_cols = self.X.select_dtypes(include=['object']).columns
            

            for col in categorical_cols:
                le = LabelEncoder()
                self.X[col] = le.fit_transform(self.X[col])
                self.label_encoders[col] = le
            logger.info("Categorical columns encoded successfully")
        except Exception as e:
            logger.error("Error in preprocessing data: %s", e)  
            raise CustomException(f"Error in preprocessing data: {e}")
    def feature_selection(self):
        try:
            X_train , _ , y_train , _ = train_test_split(self.X,self.Y , test_size=0.2 , random_state=42)
            X_cat = X_train.select_dtypes(include=['int64' , 'float64'])
            chi2_selector = SelectKBest(score_func=chi2 , k="all")
            chi2_selector.fit(X_cat,y_train)
            chi2_scores = pd.DataFrame({
                    'Feature' : X_cat.columns,
                    "Chi2 Score" : chi2_selector.scores_
                }).sort_values(by='Chi2 Score' , ascending=False)
            top_features= chi2_scores.head(5)["Feature"].tolist()
            self.selected_features = top_features
            
            self.X = self.X[self.selected_features]
            logger.info("Feature selection completed with top features")
        except Exception as e:
            logger.error("Error in feature selection: %s", e)
            raise CustomException(f"Error in feature selection: {e}")
    def split_scale_data(self):
        try:
            X_train , X_test , y_train , y_test = train_test_split(self.X,self.Y , test_size=0.2 , random_state=42 , stratify=self.Y)
            X_train = self.scaler.fit_transform(X_train)
            X_test = self.scaler.transform(X_test)
            logger.info("Data split and scaled successfully")
            return X_train, X_test, y_train, y_test
        except Exception as e:
            logger.error("Error in splitting and scaling data: %s", e)
            raise CustomException(f"Error in splitting and scaling data: {e}")
    def save_scaler_data(self,X_train, X_test, y_train, y_test):
        try:
            joblib.dump(X_train, os.path.join(self.output_path, 'X_train.pkl'))
            joblib.dump(X_test, os.path.join(self.output_path, 'X_test.pkl'))
            joblib.dump(y_train, os.path.join(self.output_path, 'y_train.pkl'))
            joblib.dump(y_test, os.path.join(self.output_path, 'y_test.pkl'))

            joblib.dump(self.scaler, os.path.join(self.output_path, 'scaler.pkl'))
            logger.info("Scaler and data saved successfully")
        except Exception as e:
            logger.error("Error saving scaler and data: %s", e)
            raise CustomException(f"Error saving scaler and data: {e}")
    def run(self):
        try:
            self.load_data()
            self.preprocess_data()
            self.feature_selection()
            X_train, X_test, y_train, y_test = self.split_scale_data()
            self.save_scaler_data(X_train, X_test, y_train, y_test)
            logger.info("Data processing completed successfully")
        except CustomException as e:
            logger.error("Data processing failed: %s", e)
            raise CustomException(f"Unexpected error during data processing: {e}")
if __name__ == "__main__":
    input_path = 'artifacts/raw/data.csv'
    output_path = 'artifacts/processed'
    data_processor = DataProcessing(input_path, output_path)
    data_processor.run()
    
