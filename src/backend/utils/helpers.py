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
        collection_name = 'fillmore'  # Nome da sua coleção
        file_field_name = 'models'  # Nome do campo de arquivo na coleção

        url = f"{POCKETBASE_URL}/api/collections/{collection_name}/records"

        files = {file_field_name: open(file_path, 'rb')}
        headers = {
            'Authorization': f'Bearer {pocketbase_token}'
        }

        response = requests.post(url, files=files, headers=headers)

        response_data = response.json()
        print(response_data)
        collectionId = response_data['collectionId']
        id = response_data['id']
        models_list = response_data['models']
        # Como 'models' é uma lista, obtenha o primeiro nome de arquivo
        file_name = models_list[0]

        if response.status_code == 200:
            return f"{POCKETBASE_URL}/api/files/{collectionId}/{id}/{file_name}"
        else:
            print(f"Error uploading file: {response.status_code}")
            print(f"Response content: {response.content}")
            return False
    except Exception as e:
        print(f"Exception during file upload: {e}")
        return False


def call_ai(df: pd.DataFrame, model):
    required_columns = ['unique_names', '1_status_10', '2_status_10', '718_status_10',
                        '1_status_13', '2_status_13']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"The input DataFrame does not have the required columns: {required_columns}")
    
    print("Data loaded successfully 2")

    input_data = df.values.astype(np.float32)

    print("Calling AI model 2...")

    input_data = np.reshape(input_data, (input_data.shape[0], input_data.shape[1]))

    print("nao deu erro")

    predictions = model.predict(input_data)

    print("Prediction result 2: ", float(predictions[0]))
    
    return float(predictions[0])

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