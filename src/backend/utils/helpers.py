import random
import time
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

model = load_model('models/model.h5')

def call_ai(df: pd.DataFrame):
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
