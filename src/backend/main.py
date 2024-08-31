from fastapi import FastAPI, UploadFile, Depends, HTTPException
import pandas as pd
import torch
import torch.nn as nn
from sqlalchemy import create_engine, Column, String, Float, Integer, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import random
import uuid
import time
from datetime import datetime, timedelta

# Configurações do banco de dados
DATABASE_URL = "postgresql://postgres:SENHA@localhost:5432/fillmore"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definição do modelo SQLAlchemy para salvar os dados
class Prediction(Base):
    __tablename__ = "predictions"
    ID = Column(String, primary_key=True, index=True)
    KNR = Column(String)
    Date = Column(String)
    unique_names = Column(Float)
    status_10_1 = Column(Float)
    status_10_2 = Column(Float)
    status_10_718 = Column(Float)
    status_13_1 = Column(Float)
    status_13_2 = Column(Float)
    status_13_718 = Column(Float)
    Prediction_result = Column(Integer)
    Real_result = Column(Integer)

# Criação da tabela no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Carregamento do modelo PyTorch
# model = torch.load('model.pt')
# model.eval()  # Configura o modelo para o modo de avaliação

# Dependência para obter a sessão do DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def call_ai(df: pd.DataFrame):
    input_data = torch.tensor(df.values, dtype=torch.float32)
    with torch.no_grad():
        predictions = model(input_data)
    return float(predictions[0].item())

def generate_uuidv7():
    timestamp_ms = int(time.time() * 1000)
    time_hex = f'{timestamp_ms:x}'
    random_hex = ''.join([f'{random.randint(0, 15):x}' for _ in range(26)])
    uuidv7 = f'{time_hex[:8]}-{time_hex[8:12]}-7{time_hex[12:15]}-{random_hex[:4]}-{random_hex[4:]}'
    return uuidv7

@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}

@app.post("/mock")
def mock_data(db: Session = Depends(get_db), num_records: int = 10):
    for _ in range(num_records):
        record = Prediction(
            ID=generate_uuidv7(),
            KNR="4321",
            Date=(datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d %H:%M:%S'),
            unique_names=random.uniform(0.0, 100.0),
            status_10_1=random.uniform(0.0, 100.0),
            status_10_2=random.uniform(0.0, 100.0),
            status_10_718=random.uniform(0.0, 100.0),
            status_13_1=random.uniform(0.0, 100.0),
            status_13_2=random.uniform(0.0, 100.0),
            status_13_718=random.uniform(0.0, 100.0),
            Prediction_result=1,
            Real_result=1
        )
        db.add(record)
    db.commit()

    return {"message": f"{num_records} records inserted successfully."}

@app.post("/predict")
async def predict(file: UploadFile, db: Session = Depends(get_db)):
    try:
        df = pd.read_csv(file.file)
        expected_columns = ['unique_names', '1_status_10', '2_status_10', '718_status_10',
                            '1_status_13', '2_status_13', '718_status_13']
        if list(df.columns) != expected_columns:
            raise HTTPException(status_code=400, detail=f"File must have the columns: {expected_columns}")

        result = call_ai(df)

        for _, row in df.iterrows():
            db_entry = Prediction(
                ID=generate_uuidv7(),
                KNR=row['unique_names'],
                Date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
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

@app.get("/predictions/")
def read_predictions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    predictions = db.query(Prediction).offset(skip).limit(limit).all()
    return predictions

@app.get("/prediction_id/{ID}")
def read_prediction(ID: str, db: Session = Depends(get_db)):
    prediction = db.query(Prediction).filter(Prediction.ID == ID).first()
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction

@app.put("/predictions/{ID}")
def update_prediction(ID: str, db: Session = Depends(get_db)):
    prediction = db.query(Prediction).filter(Prediction.ID == ID).first()
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")

    prediction.unique_names = 2.1  # Substituir com dados reais
    prediction.status_10_1 = 1.234  # Substituir com dados reais
    prediction.status_10_2 = 5.678  # Substituir com dados reais
    prediction.Prediction_result = 1  # Substituir com dados reais

    db.commit()
    db.refresh(prediction)
    return prediction

@app.delete("/predictions/{ID}")
def delete_prediction(ID: str, db: Session = Depends(get_db)):
    prediction = db.query(Prediction).filter(Prediction.ID == ID).first()
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")
    db.delete(prediction)
    db.commit()
    return {"detail": "Prediction deleted"}

@app.get("/healthcheck/model")
def healthcheck_model():
    try:
        test_prediction = 1.0 
        return {"status": "ok", "prediction": test_prediction}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/healthcheck/db")
def healthcheck_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/healthcheck/backend")
def healthcheck_backend():
    return {"status": "ok"}

