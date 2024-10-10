from fastapi import UploadFile, Depends, HTTPException, Query
import pandas as pd
import os
import random
import numpy as np
from sqlalchemy.orm import Session
from models.predictionModel import Prediction, Features, Model, Values
from models.database import get_db
from utils.helpers import call_ai, generate_uuidv7, load_model_from_url,load_model_from_path, get_model_url, authenticate_pocketbase
from typing import List
import traceback
import httpx
from io import StringIO

pocketbase_token = authenticate_pocketbase()

def root():
    return {"message": "Hello World"}

def mock_data(table: str, db: Session = Depends(get_db), num_records: int = 10):
    for _ in range(num_records):
        if table == 'Model':
            record = Model(
                ID_modelo=1,
                model='sequencial_V1',
                URL_modelo="http://pocketbase:8090/api/files/8gcjxcrdl41d3ze/wyetf08mpm5gqpe/model_URR7cOeBoC.h5"
            )
        elif table == 'Prediction':
            record = Prediction(
                KNR="2024.12",
                ID = generate_uuidv7(),
                Real_result=random.randint(0, 1),
                ID_modelo="1",
                Prediction_result=random.randint(0, 1)
            )
        db.add(record)
    db.commit()

    return {"message": f"{num_records} records inserted successfully."}

async def get_knrs(search: str = Query(None)):
    POCKETBASE_URL = "http://pocketbase:8090/api/files/8gcjxcrdl41d3ze/eyiqehnwwe7oy68/small_data_gGUzmjNESd.csv"
    try:
        # Download the CSV file from the U  RL
        async with httpx.AsyncClient() as client:
            response = await client.get(POCKETBASE_URL)

        # Check if the download was successful
        if response.status_code == 200:
            # Convert the downloaded CSV content to a Pandas DataFrame
            csv_content = response.content.decode('utf-8')
            df = pd.read_csv(StringIO(csv_content))

            if search:
                # Filter KNRs that contain the search term (case-insensitive)
                filtered_knrs = df[df['KNR'].str.contains(search, case=False, na=False)]['KNR'].unique().tolist()
                # Limit the number of KNRs returned
                filtered_knrs = filtered_knrs[:50]  # Return up to 50 KNRs
            else:
                filtered_knrs = []

            return {"knrs": filtered_knrs}
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to download CSV from Pocketbase")

    except Exception as e:
        print(f"Error in /knrs endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
async def predict(knr: str, db: Session = Depends(get_db)):
    POCKETBASE_CSV_URL = "http://pocketbase:8090/api/files/8gcjxcrdl41d3ze/eyiqehnwwe7oy68/small_data_gGUzmjNESd.csv"
    try:
        print("Predicting...")
        
        # Load the model from local path (this remains the same)
        model_path = os.path.join("models", "model.h5")
        print("Model URL:", model_path)

        model = load_model_from_path(model_path)
        print("Model loaded successfully")

        # Download the CSV file from Pocketbase URL
        print(f"Downloading CSV file from: {POCKETBASE_CSV_URL}")
        async with httpx.AsyncClient() as client:
            response = await client.get(POCKETBASE_CSV_URL)

        if response.status_code == 200:
            # Convert the downloaded CSV content to a Pandas DataFrame
            csv_content = response.content.decode('utf-8')
            df = pd.read_csv(StringIO(csv_content))
            print("CSV file loaded.")
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to download CSV from Pocketbase")

        # Verify that KNR exists
        if knr not in df['KNR'].values:
            print(f"KNR {knr} not found in CSV.")
            raise HTTPException(status_code=404, detail=f"KNR {knr} not found in data.")

        # Filter the DataFrame to the selected KNR
        df_knr = df[df['KNR'] == knr]
        print(f"Data for KNR {knr}:\n{df_knr}")

        # Print the columns in df_knr
        print(f"Columns in df_knr: {df_knr.columns.tolist()}")

        # Define expected columns based on your CSV
        expected_columns = ['unique_names', '1_status_10', '2_status_10', '718_status_10',
                            '1_status_13', '2_status_13', '718_status_13',
                            '_unit_count', '%_unit_count', 'Clicks_unit_count', 'Deg_unit_count',
                            'Grad_unit_count', 'Nm_unit_count', 'Unnamed: 5_unit_count',
                            'V_unit_count', 'kg_unit_count', 'min_unit_count', 'mm_unit_count',
                            '_unit_mean', '%_unit_mean', 'Clicks_unit_mean', 'Deg_unit_mean',
                            'Grad_unit_mean', 'Nm_unit_mean', 'Unnamed: 5_unit_mean',
                            'V_unit_mean', 'kg_unit_mean', 'min_unit_mean', 'mm_unit_mean']

        # Check for missing columns
        missing_columns = set(expected_columns) - set(df_knr.columns)
        if missing_columns:
            print(f"Missing columns: {missing_columns}")
            # Handle missing columns by adding them with default values
            for col in missing_columns:
                df_knr[col] = 0  # or an appropriate default value
            print(f"Added missing columns with default values.")

        # Ensure columns are in the correct order
        features_df = df_knr[expected_columns]
        print("Features for prediction:")
        print(features_df)

        # Convert features to float32
        try:
            features_df = features_df.astype(np.float32)
        except ValueError as ve:
            print(f"Data type conversion error: {ve}")
            raise HTTPException(status_code=400, detail=f"Data type conversion error: {ve}")

        # Check for NaN values
        if features_df.isnull().values.any():
            print("Warning: features_df contains NaN or missing values.")
            print(features_df.isnull().sum())
            # Handle NaNs if necessary
            features_df = features_df.fillna(0)

        print("Calling AI model...")

        # Call the AI model
        result = call_ai(features_df, model)
        print("Prediction result:", result)

        # Database operations (if any)
        # ... (existing code for inserting prediction into the database)

        return {"prediction": result}

    except HTTPException as http_exc:
        print(f"HTTPException: {http_exc.detail}")
        traceback.print_exc()
        db.rollback()
        raise http_exc
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


def read_predictions(table: str, skip: int, limit: int, db: Session = Depends(get_db)) -> List[dict]:

    table_map = {
        'Prediction': Prediction,
        'Features': Features,
        'Model': Model,
        'Values': Values
    }
    
    if table not in table_map:
        raise HTTPException(status_code=400, detail=f"Table '{table}' not recognized.")
    
    model_class = table_map[table]
    
    records = db.query(model_class).offset(skip).limit(limit).all()
    
    result = [record.__dict__ for record in records]
    
    for record in result:
        record.pop('_sa_instance_state', None)
    
    return result

def read_prediction(ID: str, db: Session = Depends(get_db)):
    prediction = db.query(Prediction).filter(Prediction.ID == ID).first()
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction

def update_prediction(ID: str, db: Session = Depends(get_db)):
    prediction = db.query(Prediction).filter(Prediction.ID == ID).first()
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")

    prediction.KNR = "Updated KNR"
    prediction.Prediction_result = 1
    
    db.commit()
    db.refresh(prediction)
    return prediction

def delete_prediction(ID: str, db: Session = Depends(get_db)):
    prediction = db.query(Prediction).filter(Prediction.ID == ID).first()
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")
    db.delete(prediction)
    db.commit()
    return {"detail": "Prediction deleted"}

def update_model(ID: str, db: Session = Depends(get_db)):
    record = db.query(Model).filter(Model.ID_modelo == ID).first()

    if not record:
        raise HTTPException(status_code=404, detail="Model not found")

    features = [
        1,
        2,
        3,
        4,
        5,
        6
    ]

    record.precision = 0.90
    record.features = features
    
    db.commit()  
    db.refresh(record)  

    return record  