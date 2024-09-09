from fastapi import UploadFile, Depends, HTTPException
import pandas as pd
import random
import numpy as np
from sqlalchemy.orm import Session
from models.predictionModel import Prediction, Features, Model, Values
from models.database import get_db
from tensorflow.keras.models import load_model
from utils.helpers import call_ai, generate_uuidv7
from typing import List

model = load_model('models/model.h5')

def root():
    return {"message": "Hello World"}

def mock_data(table:str , db: Session = Depends(get_db), num_records: int = 10):
    for _ in range(num_records):
        if table == 'Model':
            record = Model(
                ID_modelo=1,
                model='progression_V1',
                URL_modelo="http://example.com/model_1"
            )
        db.add(record)
    db.commit()

    return {"message": f"{num_records} records inserted successfully."}

async def predict(file: UploadFile, db: Session = Depends(get_db)):
    try:
        df = pd.read_csv(file.file)
        expected_columns = ['KNR','unique_names', '1_status_10', '2_status_10', '718_status_10',
                            '1_status_13', '2_status_13', '718_status_13']
        if list(df.columns) != expected_columns:
            raise HTTPException(status_code=400, detail=f"File must have the columns: {expected_columns}")
        
        knr = df['KNR'].iloc[0]
        df = df.drop(columns=['KNR'])

        result = call_ai(df)

        for _, row in df.iterrows():
            db_entry = Prediction(
                ID=generate_uuidv7(),
                KNR=knr,
                unique_names=row['unique_names'],
                status_10_1=row['1_status_10'],
                status_10_2=row['2_status_10'],
                status_10_718=row['718_status_10'],
                status_13_1=row['1_status_13'],
                status_13_2=row['2_status_13'],
                status_13_718=row['718_status_13'],
                Prediction_result=int(result),
                Real_result=random.randint(0, 1)
            )
            db.add(db_entry)
        db.commit()

        return {"prediction": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

def read_predictions(table: str, skip: int, limit: int, db: Session = Depends(get_db)) -> List[dict]:
    # Map table names to their corresponding SQLAlchemy model classes
    table_map = {
        'Prediction': Prediction,
        'Features': Features,
        'Model': Model,
        'Values': Values
    }
    
    # Check if the table exists in the table map
    if table not in table_map:
        raise HTTPException(status_code=400, detail=f"Table '{table}' not recognized.")
    
    # Get the model class corresponding to the table name
    model_class = table_map[table]
    
    # Query the database for the specified table
    records = db.query(model_class).offset(skip).limit(limit).all()
    
    # Convert the SQLAlchemy objects to dictionaries for better display
    result = [record.__dict__ for record in records]
    
    # Remove the SQLAlchemy internal state from the dictionary
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

    prediction.unique_names = 2.1
    prediction.status_10_1 = 1.234
    prediction.status_10_2 = 5.678
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