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

def mock_data(table: str, db: Session = Depends(get_db), num_records: int = 10):
    for _ in range(num_records):
        if table == 'Model':
            record = Model(
                ID_modelo=generate_uuidv7(),
                model='sequencial_V1',
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

        prediction_id = generate_uuidv7()
        for _, row in df.iterrows():
            prediction_entry = Prediction(
                ID=prediction_id,
                KNR=knr,
                ID_modelo="1", 
                Prediction_result=int(result),
                Real_result=random.randint(0, 1)
            )
            db.add(prediction_entry)

            features = [
                ('1_status_10', row['1_status_10']),
                ('2_status_10', row['2_status_10']),
                ('718_status_10', row['718_status_10']),
                ('1_status_13', row['1_status_13']),
                ('2_status_13', row['2_status_13']),
                ('718_status_13', row['718_status_13']),
            ]

            for feature_name, feature_value in features:
                feature = db.query(Features).filter(Features.name_feature == feature_name).first()
                if not feature:
                    feature = Features(name_feature=feature_name)
                    db.add(feature)
                    db.commit()  

                values_entry = Values(
                    ID_feature=feature.ID_feature,
                    ID=prediction_id,
                    ID_modelo="1",  
                    value_feature=feature_value
                )
                db.add(values_entry)

        db.commit()

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
