from fastapi import FastAPI, UploadFile, Depends, HTTPException
import pandas as pd
import torch
import torch.nn as nn
from sqlalchemy import create_engine, Column, Integer, String , Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import uuid
import time
import random

DATABASE_URL = "postgresql://postgres:SENHA@localhost:5432/fillmore"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define a SQLAlchemy model to save the data
class Prediction(Base):

    # Please change all of this with the actual structure of the database
    __tablename__ = "prediction_data"

    ID = Column(String, primary_key=True, index=True, autoincrement=True)
    KNR = Column(String)
    Date = Column(Float)
    Feature1 = Column(Float)
    Feature2 = Column(Float)
    Feature3 = Column(Float)
    Prediction_result = Column(Integer)
    Real_result = Column(Integer)

# Create the table in the database
Base.metadata.create_all(bind=engine)


app = FastAPI()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# class MyModel(nn.Module):
#     def __init__(self):
#         super(MyModel, self).__init__()
#         # This is just an example. Please change it to what matches your model
#         self.fc1 = nn.Linear(10, 50)
#         self.relu = nn.ReLU()
#         self.fc2 = nn.Linear(50, 20)
#         self.fc3 = nn.Linear(20, 1)

#     def forward(self, x):
#         # Just another example again. Please change it
#         x = self.fc1(x)
#         x = self.relu(x)
#         x = self.fc2(x)
#         x = self.relu(x)
#         x = self.fc3(x)
#         return x  # Replace with your forward pass logic

# model = MyModel()
# model.eval()

# def call_ai(df: pd.DataFrame):
#     # Step 1: Convert the DataFrame to a tensor
#     # Assuming df has the required 10 features
#     input_tensor = torch.tensor(df.values, dtype=torch.float32)

#     # Step 2: Ensure the input tensor has the correct shape
#     if input_tensor.ndimension() == 1:
#         input_tensor = input_tensor.unsqueeze(0)  # Add batch dimension if needed

#     # Step 3: Get the prediction
#     with torch.no_grad():  # Disable gradient calculations for inference
#         prediction = model(input_tensor)

#     # Step 4: Return the prediction as a scalar
#     return prediction.item()

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
async def root():
    return {"message": "Hello World"}

#-Caso não divida em 2 modelos
# @app.post("/predict")
# async def predict(file: UploadFile, db: Session = Depends(get_db)):
#     df = pd.read_csv(file.file)
#     result = call_ai(df)

#     # Save the data and prediction to the database
#     for _, row in df.iterrows():
#         db_entry = Prediction(
#             feature1=row[0],  # Replace with your actual column mappings
#             feature2=row[1],
#             feature3=row[2],
#             # Continue for all features
#             prediction_result=result
#         )
#         db.add(db_entry)
#     db.commit()

#     return {"prediction": result}

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

@app.get("/predictions/{prediction_id}")
def read_prediction(prediction_id: String, db: Session = Depends(get_db)):
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction

@app.put("/predictions/{prediction_id}")
def update_prediction(prediction_id: int, db: Session = Depends(get_db)):
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")

    # Aqui você faria a atualização com novos valores, que podem ser extraídos de algum lugar (ex: request body)
    # Por exemplo, aqui podemos usar dados fictícios, mas eles deveriam vir de algum lugar válido
    prediction.feature1 = "new_value1"
    prediction.feature2 = 1.234
    prediction.feature3 = 5.678
    prediction.prediction_result = 9.1011

    db.commit()
    db.refresh(prediction)
    return prediction

@app.delete("/predictions/{prediction_id}")
def delete_prediction(prediction_id: int, db: Session = Depends(get_db)):
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")
    db.delete(prediction)
    db.commit()
    return {"detail": "Prediction deleted"}

@app.get("/healthcheck/model")
def healthcheck_model():
    try:
        test_prediction = 1.0  # Simulação de predição de teste
        return {"status": "ok", "prediction": test_prediction}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/healthcheck/db")
def healthcheck_db(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/healthcheck/backend")
def healthcheck_backend():
    return {"status": "ok"}
