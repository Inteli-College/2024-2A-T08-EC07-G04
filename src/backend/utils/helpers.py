import random
import time
import numpy as np
import pandas as pd
import os
import requests
import tensorflow as tf
from tensorflow.keras.models import load_model
from models.predictionModel import Model
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from models.database import get_db
import os
import logging

logger = logging.getLogger(__name__)

def authenticate_pocketbase():
    POCKETBASE_URL = "http://pocketbase:8090"
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

def upload_model_to_pocketbase(file_path: str) -> str:
    try:
        POCKETBASE_URL = "http://pocketbase:8090"
        collection_name = 'fillmore'  # Name of your collection
        file_field_name = 'field'  # Field name based on your image

        url = f"{POCKETBASE_URL}/api/collections/{collection_name}/records"

        files = {file_field_name: open(file_path, 'rb')}
        headers = {
            'Authorization': f'Bearer {pocketbase_token}'
        }

        response = requests.post(url, files=files, headers=headers)
        response_data = response.json()

        print(f"Response data: {response_data}")

        if response.status_code == 200:
            collectionId = response_data['collectionId']
            id = response_data['id']
            models_list = response_data[file_field_name]  # Update to use correct field
            file_name = models_list[0]  # Assuming it's a list of filenames

            return f"{POCKETBASE_URL}/api/files/{collectionId}/{id}/{file_name}"
        else:
            print(f"Error uploading file: {response.status_code}")
            print(f"Response content: {response.content}")
            return False
    except Exception as e:
        print(f"Exception during file upload: {e}")
        return False


def call_ai(df: pd.DataFrame, model):
    """
    Prepares the input data and calls the AI model to make a prediction.
    """
    try:
        expected_columns = [
            'unique_names', '1_status_10', '2_status_10', '718_status_10',
            '1_status_13', '2_status_13', '718_status_13',
            '_unit_count', '%_unit_count', 'Clicks_unit_count', 'Deg_unit_count',
            'Grad_unit_count', 'Nm_unit_count', 'Unnamed: 5_unit_count',
            'V_unit_count', 'kg_unit_count', 'min_unit_count', 'mm_unit_count',
            '_unit_mean', '%_unit_mean', 'Clicks_unit_mean', 'Deg_unit_mean',
            'Grad_unit_mean', 'Nm_unit_mean', 'Unnamed: 5_unit_mean',
            'V_unit_mean', 'kg_unit_mean', 'min_unit_mean', 'mm_unit_mean'
        ]  # Updated expected columns

        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"The input DataFrame is missing required columns: {missing_columns}")
        
        print("Data loaded successfully.")

        # Ensure the data is in the correct order and data type
        input_data = df[expected_columns].astype(np.float32).values

        print("Calling AI model...")

        # Adjust the input shape to match the model's expected input shape
        # The model expects input shape of (batch_size, time_steps, features)
        # In this case, time_steps = 1
        input_data = np.expand_dims(input_data, axis=1)  # Adds a new dimension at axis=1

        print(f"Adjusted input shape: {input_data.shape}")

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


def load_model_from_url(url: str):
    unique_filename = f"temp_model_{generate_uuidv7()}.h5"
    
    headers = {
        'Authorization': f'Bearer {pocketbase_token}'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to download the model.")
    
    with open(unique_filename, "wb") as f:
        f.write(response.content)
    
    model = tf.keras.models.load_model(unique_filename)
    
    os.remove(unique_filename)

    print("Model loaded successfully")
    
    return model



def get_model_url(ID_modelo: str, db: Session = Depends(get_db)) -> str:
    record = db.query(Model).filter(Model.ID_modelo == ID_modelo).first()

    if not record:
        raise HTTPException(status_code=404, detail="Model not found")

    url_modelo = record.URL_modelo

    return url_modelo

def load_model_from_path(model_path: str):
    """
    Loads the model from a given file path.
    """
    try:
        print(f"Loading model from: {model_path}")
        if not os.path.exists(model_path):
            print(f"Model file not found at path: {model_path}")
            raise HTTPException(status_code=404, detail="Model file not found.")
        model = load_model(model_path)
        print("Model loaded successfully.")
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")