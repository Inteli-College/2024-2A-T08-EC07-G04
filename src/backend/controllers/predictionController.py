from fastapi import UploadFile, Depends, HTTPException
import pandas as pd
import random
import numpy as np
from sqlalchemy.orm import Session
from models.predictionModel import Prediction, Features, Model, Values
from models.database import get_db
from utils.helpers import call_ai, generate_uuidv7, load_model_from_url, get_model_url
from typing import List
import requests

# PocketBase configuration
POCKETBASE_URL = "http://pocketbase:8090"


def authenticate_pocketbase():
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

# Initialize PocketBase authentication (you can save this token for further requests)
pocketbase_token = authenticate_pocketbase()

def root():
    return {"message": "Hello World"}

def mock_data(table: str, db: Session = Depends(get_db), num_records: int = 10):
    for _ in range(num_records):
        if table == 'Model':
            record = Model(
                ID_modelo=1,
                model='sequencial_V1',
                URL_modelo="http://pocketbase:8090/api/files/4forqd5s2ez9ydw/wwpjocvw1obr90r/modelo_0cJQGhMAmk.h5"
            )
        db.add(record)
    db.commit()

    return {"message": f"{num_records} records inserted successfully."}

async def predict(file: UploadFile, id_modelo:str, db: Session = Depends(get_db)):
    try:
        print("Predicting...")
        model_url = get_model_url(id_modelo, db)
        print("Model URL: ", model_url)

        model = load_model_from_url(model_url)
        print("Model loaded successfully")

        df = pd.read_csv(file.file)
        expected_columns = ['KNR','unique_names', '1_status_10', '2_status_10', '718_status_10',
                            '1_status_13', '2_status_13', '718_status_13']
        if list(df.columns) != expected_columns:
            raise HTTPException(status_code=400, detail=f"File must have the columns: {expected_columns}")
        
        print("Data loaded successfully")

        knr = df['KNR'].iloc[0]
        df = df.drop(columns=['KNR'])

        print("Calling AI model...")

        result = call_ai(df, model)

        print("Prediction result: ", result)

        # prediction_id = generate_uuidv7()
        # for _, row in df.iterrows():
        #     prediction_entry = Prediction(
        #         ID=prediction_id,
        #         KNR=knr,
        #         ID_modelo="1", 
        #         Prediction_result=int(result),
        #         Real_result=random.randint(0, 1)
        #     )
        #     db.add(prediction_entry)

        #     features = [
        #         ('1_status_10', row['1_status_10']),
        #         ('2_status_10', row['2_status_10']),
        #         ('718_status_10', row['718_status_10']),
        #         ('1_status_13', row['1_status_13']),
        #         ('2_status_13', row['2_status_13']),
        #         ('718_status_13', row['718_status_13']),
        #     ]

        #     for feature_name, feature_value in features:
        #         feature = db.query(Features).filter(Features.name_feature == feature_name).first()
        #         if not feature:
        #             feature = Features(name_feature=feature_name)
        #             db.add(feature)
        #             db.commit()  

        #         values_entry = Values(
        #             ID_feature=feature.ID_feature,
        #             ID=prediction_id,
        #             ID_modelo="1",  
        #             value_feature=feature_value
        #         )
        #         db.add(values_entry)

        # db.commit()

        return {"prediction": result}

    except Exception as e:
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
    # Fetch the record to update by ID
    record = db.query(Model).filter(Model.ID_modelo == ID).first()

    if not record:
        raise HTTPException(status_code=404, detail="Model not found")

    # Update the record with new values
    record.model = 'sequencial_V1'
    record.URL_modelo = "http://pocketbase:8090/api/files/4forqd5s2ez9ydw/nel4f0k3tw7k8uq/model_VCjEboMsys.h5"
    
    db.commit()  # Commit the transaction to save the changes
    db.refresh(record)  # Optional: Refresh the instance with the latest data from the database

    return record  # Optionally return the updated record
