import random
import time
import numpy as np
import pandas as pd
import os
import requests
import tensorflow as tf
from models.predictionModel import Model
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from models.database import get_db
from tensorflow.keras.models import load_model
import os
import logging
import traceback

logger = logging.getLogger(__name__)

POCKETBASE_URL = "http://pocketbase:8090"

def authenticate_pocketbase():
    pass
    try:
        auth_data = {
            "identity": "teste@gmail.com",
            "password": "testeteste"
        }
        response = requests.post(f"{POCKETBASE_URL}/api/admins/auth-with-password", json=auth_data)

        if response.status_code == 200:
            print("Authenticated successfully!")
            return response.json()["token"]
        else:
            raise HTTPException(status_code=response.status_code, detail="Authentication failed.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
    
    
pocketbase_token = authenticate_pocketbase()

def upload_model_to_pocketbase(file_path: str, token: str) -> str:
    try:
        POCKETBASE_URL = "http://pocketbase:8090"
        collection_name = 'fillmore'  # Nome da sua coleção
        file_field_name = 'model_file'  # Nome do campo de arquivo na coleção

        url = f"{POCKETBASE_URL}/api/collections/{collection_name}/records"

        files = {file_field_name: open(file_path, 'rb')}
        headers = {
            'Authorization': f'Admin {token}'
        }

        response = requests.post(url, files=files, headers=headers)
        response.raise_for_status()

        # Extrair a URL do arquivo a partir da resposta
        record = response.json()
        file_id = record['id']
        file_name = record[file_field_name]

        file_url = f"{POCKETBASE_URL}/api/files/{collection_name}/{file_id}/{file_name}"

        print(f"Model uploaded to PocketBase successfully. URL: {file_url}")
        return file_url  # Retorna apenas a URL como string
    except requests.HTTPError as e:
        print(f"Error uploading file: {e.response.status_code}")
        print(f"Response content: {e.response.content}")
        raise Exception("Failed to upload the model to PocketBase.")
    except Exception as e:
        print(f"Exception during file upload: {e}")
        raise Exception("Failed to upload the model to PocketBase.")


def call_ai(df: pd.DataFrame, model):
    """
    Prepares the input data and calls the AI model to make a prediction.
    """
    try:
        expected_columns = ['unique_names', '1_status_10', '2_status_10', '718_status_10',
                            '1_status_13', '2_status_13', '718_status_13',
                            '_unit_count', '%_unit_count', 'Clicks_unit_count', 'Deg_unit_count',
                            'Grad_unit_count', 'Nm_unit_count', 'Unnamed: 5_unit_count',
                            'V_unit_count', 'kg_unit_count', 'min_unit_count', 'mm_unit_count',
                            '_unit_mean', '%_unit_mean', 'Clicks_unit_mean', 'Deg_unit_mean',
                            'Grad_unit_mean', 'Nm_unit_mean', 'Unnamed: 5_unit_mean',
                            'V_unit_mean', 'kg_unit_mean', 'min_unit_mean', 'mm_unit_mean']  # Updated expected columns

        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"The input DataFrame is missing required columns: {missing_columns}")
        
        print("Data loaded successfully.")

        # Ensure the data is in the correct order
        input_data = df[expected_columns].astype(np.float32).values

        print("Calling AI model...")

        # Adjust the input shape if necessary
        # For example, if the model expects (1, num_features)
        if len(input_data.shape) == 1:
            input_data = np.expand_dims(input_data, axis=0)

        predictions = model.predict(input_data)

        # Process the prediction output
        # Assuming the model outputs a scalar value per input
        prediction_result = float(predictions[0][0])  # Adjust indexing based on model output shape

        print(f"Prediction result: {prediction_result}")

        return prediction_result
    except Exception as e:
        print(f"Error during model prediction: {str(e)}")
        raise

def generate_uuidv7():
    # Get the current timestamp in milliseconds
    timestamp_ms = int(time.time() * 1000)
    
    # Convert the timestamp to a hex string and ensure it is 12 characters long
    time_hex = f'{timestamp_ms:012x}'
    
    # Generate 10 random hex characters for the random portion of the UUID
    random_hex = ''.join([f'{random.randint(0, 15):x}' for _ in range(10)])
    
    # Construct the UUIDv7 string with version 7 and proper structure
    uuidv7 = f'{time_hex[:8]}-{time_hex[8:12]}-7{random_hex[:3]}-{random_hex[3:7]}-{random_hex[7:]}'
    
    return uuidv7




def load_model_from_url(model_path):
    try:
        print(f"Loading model from: {model_path}")
        model = load_model(model_path)
        print("Model loaded successfully.")
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise


def get_model_url(ID_modelo: str, db: Session = Depends(get_db)) -> str:
    record = db.query(Model).filter(Model.ID_modelo == ID_modelo).first()

    if not record:
        raise HTTPException(status_code=404, detail="Model not found")

    url_modelo = record.URL_modelo

    return url_modelo