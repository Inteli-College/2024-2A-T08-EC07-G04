from fastapi import FastAPI, UploadFile, Depends, HTTPException
import pandas as pd
import torch
import torch.nn as nn
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import random
import time
from datetime import datetime, timedelta
import uuid
import numpy as np

DATABASE_URL = "postgresql://postgres:SENHA@localhost:5432/fillmore"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define a SQLAlchemy model to save the data
class Prediction(Base):
    __tablename__ = "teste"

    ID = Column(String, primary_key=True, index=True)
    ID = Column(Integer, primary_key=True, index=True)
    KNR = Column(String)
    Date = Column(String)
    Feature1 = Column(Float)
    Feature2 = Column(Float)
    Feature3 = Column(Float)
    Prediction_result = Column(Integer)
    Real_result = Column(Integer)

# Create the table in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Load the PyTorch model
# model = torch.load('model.pt')
# model.eval()  # Set the model to evaluation mode

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def call_ai(df: pd.DataFrame):
#     # Convert the DataFrame to a tensor
#     input_data = torch.tensor(df.values, dtype=torch.float32)
    
#     # Run the model prediction
#     with torch.no_grad():  # Disable gradient calculations for inference
#         predictions = model(input_data)
    
#     # If your model returns a scalar value directly:
#     return float(predictions[0].item())  # Convert the tensor to a Python float

def generate_uuidv7():
    # Obtém o timestamp atual em milissegundos
    timestamp_ms = int(time.time() * 1000)
    
    # Converte o timestamp para hexadecimal
    time_hex = f'{timestamp_ms:x}'
    
    # Gera a parte aleatória do UUID
    random_hex = ''.join([f'{random.randint(0, 15):x}' for _ in range(26)])
    
    # Constrói o UUIDv7 concatenando as partes (versão 7 indica com '7' no início da terceira parte)
    uuidv7 = f'{time_hex[:8]}-{time_hex[8:12]}-7{time_hex[12:15]}-{random_hex[:4]}-{random_hex[4:]}'
    
    return uuidv7

@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}

@app.post("/mock")
def mock_data(db: Session = Depends(get_db), num_records: int = 10):
    record = Prediction(
        ID=generate_uuidv7(),
        KNR="4321",
        Date=(datetime.now() - timedelta(days=random.randint(0, 365))).timestamp(),
        Feature1=random.uniform(0.0, 100.0),
        Feature2=random.uniform(0.0, 100.0),
        Feature3=random.uniform(0.0, 100.0),
        Prediction_result=1,
        Real_result=1
    )
    
    db.add(record)
    db.commit()

    return {"message": f"{num_records} records inserted successfully."}

# @app.post("/predict")
# async def predict(file: UploadFile, db: Session = Depends(get_db)):
#     try:
#         # Step 1: Read the uploaded file into a DataFrame
#         df = pd.read_csv(file.file)

#         # Step 2: Ensure the DataFrame has the correct number of features (adjust as needed)
#         if len(df.columns) != 10:
#             raise HTTPException(status_code=400, detail="File must have 10 columns")

#         # Step 3: Call the AI inference function
#         result = call_ai(df)

#         # Step 4: Save the data and prediction to the database
#         for _, row in df.iterrows():
#             db_entry = Prediction(
#                 KNR=row[0],
#                 Date=row[1],
#                 Feature1=row[2],
#                 Feature2=row[3],
#                 Feature3=row[4],
#                 Prediction_result=result,
#                 Real_result=random.randint(0, 1)  # Replace with actual data if needed
#             )
#             db.add(db_entry)
#         db.commit()

#         return {"prediction": result}

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# To run the app:
# uvicorn main:app --reload

#-Caso a gente divida em 2 modelos
# @app.post("/predict_binary")
# async def predict_binary (file: UploadFile):
# 	df = pd.read_csv(file.file)
# 	result = call_ai_binary(df)
# 	if result is False:
# 		return {"prediction": result}
# 	if result:
# 		result = call_ai_fail(df)
# 		return {"prediction": result}

@app.get("/predictions/")
def read_predictions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    predictions = db.query(Prediction).offset(skip).limit(limit).all()
    return predictions

# @app.get("/predictions/{prediction_id}")
# def read_prediction(prediction_id: String, db: Session = Depends(get_db)):
#     prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
#     if prediction is None:
#         raise HTTPException(status_code=404, detail="Prediction not found")
#     return prediction

# @app.put("/predictions/{prediction_id}")
# def update_prediction(prediction_id: String, db: Session = Depends(get_db)):
#     prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
#     if prediction is None:
#         raise HTTPException(status_code=404, detail="Prediction not found")

#     # Aqui você faria a atualização com novos valores, que podem ser extraídos de algum lugar (ex: request body)
#     # Por exemplo, aqui podemos usar dados fictícios, mas eles deveriam vir de algum lugar válido
#     prediction.feature1 = "new_value1"
#     prediction.feature2 = 1.234
#     prediction.feature3 = 5.678
#     prediction.prediction_result = 9.1011

#     db.commit()
#     db.refresh(prediction)
#     return prediction

# @app.delete("/predictions/{prediction_id}")
# def delete_prediction(prediction_id: String, db: Session = Depends(get_db)):
#     prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
#     if prediction is None:
#         raise HTTPException(status_code=404, detail="Prediction not found")
#     db.delete(prediction)
#     db.commit()
#     return {"detail": "Prediction deleted"}

@app.get("/healthcheck/model")
def healthcheck_model():
    try:
        test_prediction = 1.0  # Simulação de predição de teste
        return {"status": "ok", "prediction": test_prediction}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# @app.get("/healthcheck/db")
# def healthcheck_db(db: Session = Depends(get_db)):
#     try:
#         db.execute("SELECT 1")
#         return {"status": "ok"}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

@app.get("/healthcheck/backend")
def healthcheck_backend():
    return {"status": "ok"}
