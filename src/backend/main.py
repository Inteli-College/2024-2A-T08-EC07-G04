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
from tensorflow.keras.models import load_model
import numpy as np

DATABASE_URL = "postgresql://postgres:SENHA@localhost:5432/fillmore"
 
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definição do modelo SQLAlchemy para salvar os dados
class Prediction(Base):
    __tablename__ = "table"
    ID = Column(String, primary_key=True, index=True)
    KNR = Column(String)
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

# Registro das rotas
app.include_router(predictionRoutes.router)
app.include_router(healthChecksRoutes.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

