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
import os
import tempfile
import logging

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
    
pocketbase_tocken = authenticate_pocketbase()

def upload_model_to_pocketbase(file_path: str, token: str) -> str:
    try:
        collection_name = 'models'
        files = {
            'file': open(file_path, 'rb')
        }
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = requests.post(
            f"{POCKETBASE_URL}/api/collections/{collection_name}/records",
            files=files,
            headers=headers
        )
        response.raise_for_status()
        file_info = response.json()
        file_url = f"{POCKETBASE_URL}/api/files/{collection_name}/{file_info['id']}/{file_info['file']}"
        logger.info(f"Model uploaded to PocketBase successfully. URL: {file_url}")
        return file_url
    except Exception as e:
        logger.error(f"Failed to upload model to PocketBase: {e}")
        raise Exception("Model upload to PocketBase failed.")


def call_ai(df: pd.DataFrame, model):
    required_columns = ['unique_names', '1_status_10', '2_status_10', '718_status_10',
                        '1_status_13', '2_status_13']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"The input DataFrame does not have the required columns: {required_columns}")
    
    input_data = df.values.astype(np.float32)
    input_data = np.reshape(input_data, (input_data.shape[0], input_data.shape[1]))

    predictions = model.predict(input_data)
    return float(predictions[0])

def generate_uuidv7():
    timestamp_ms = int(time.time() * 1000)
    time_hex = f'{timestamp_ms:x}'
    random_hex = ''.join([f'{random.randint(0, 15):x}' for _ in range(26)])
    uuidv7 = f'{time_hex[:8]}-{time_hex[8:12]}-7{time_hex[12:15]}-{random_hex[:4]}-{random_hex[4:]}'
    return uuidv7

def load_model_from_url(url: str):
    try:
        with tempfile.NamedTemporaryFile(suffix='.h5', delete=False) as tmp_file:
            response = requests.get(url)
            response.raise_for_status()
            tmp_file.write(response.content)
            temp_filename = tmp_file.name

        model = tf.keras.models.load_model(temp_filename)
        logger.info("Model loaded successfully from URL.")
        return model
    except Exception as e:
        logger.error(f"Failed to load model from URL: {e}")
        raise Exception("Failed to load model.")
    finally:
        if 'temp_filename' in locals() and os.path.exists(temp_filename):
            os.remove(temp_filename)


def get_model_url(ID_modelo: str, db: Session = Depends(get_db)) -> str:
    record = db.query(Model).filter(Model.ID_modelo == ID_modelo).first()

    if not record:
        raise HTTPException(status_code=404, detail="Model not found")

    url_modelo = record.URL_modelo

    return url_modelo