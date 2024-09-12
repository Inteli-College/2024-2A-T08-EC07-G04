import random
import time
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import os
import requests
import tensorflow as tf
from models.predictionModel import Model
from sqlalchemy.orm import Session


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
    # Generate a unique file name for the model
    unique_filename = f"temp_model_{generate_uuidv7().hex}.h5"
    
    # Download the model from the URL
    response = requests.get(url)
    with open(unique_filename, "wb") as f:
        f.write(response.content)
    
    # Load the model
    model = tf.keras.models.load_model(unique_filename)
    
    # Optionally, remove the file after loading the model to clean up
    os.remove(unique_filename)
    
    return model

def get_model_url(db: Session, id_modelo: str) -> str:
    # Query the Model table for the URL_modelo using the provided ID_modelo
    model_record = db.query(Model).filter(Model.ID_modelo == id_modelo).first()
    
    if model_record is None:
        raise HTTPException(status_code=404, detail="Model ID not found")
    
    return model_record.URL_modelo