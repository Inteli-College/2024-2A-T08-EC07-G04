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

# Configurações do banco de dados
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

# Carregamento do modelo de machine learning
model = load_model('model/model.h5')

# Dependência para obter a sessão do DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função que realiza a previsão utilizando o modelo de machine learning
def call_ai(df: pd.DataFrame):
    required_columns = ['unique_names', '1_status_10', '2_status_10', '718_status_10',
                        '1_status_13', '2_status_13']  # Verifica se as colunas necessárias estão presentes
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"The input DataFrame does not have the required columns: {required_columns}")
    
    input_data = df.values.astype(np.float32)  # Converte os dados do DataFrame para float32
    
    input_data = np.reshape(input_data, (input_data.shape[0], input_data.shape[1]))  # Redimensiona os dados para o formato esperado pelo modelo

    predictions = model.predict(input_data)  # Faz a previsão usando o modelo carregado
    return float(predictions[0])

# Função para gerar um UUIDv7
def generate_uuidv7():
    timestamp_ms = int(time.time() * 1000)  # Obtém o timestamp em milissegundos
    time_hex = f'{timestamp_ms:x}'  # Converte o timestamp para hexadecimal
    random_hex = ''.join([f'{random.randint(0, 15):x}' for _ in range(26)])  # Gera uma parte aleatória em hexadecimal
    uuidv7 = f'{time_hex[:8]}-{time_hex[8:12]}-7{time_hex[12:15]}-{random_hex[:4]}-{random_hex[4:]}'  # Formata o UUIDv7
    return uuidv7

# Rota principal que retorna uma mensagem de "Hello World"
@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}

# Rota para inserir dados fictícios no banco de dados
@app.post("/mock")
def mock_data(db: Session = Depends(get_db), num_records: int = 10):
    for _ in range(num_records):  # Insere `num_records` registros fictícios na tabela Prediction
        record = Prediction(
            ID=generate_uuidv7(),
            KNR="4321",
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
        db.add(record)  # Adiciona o registro ao banco de dados
    db.commit()  # Confirma as alterações no banco de dados

    return {"message": f"{num_records} records inserted successfully."}

# Rota para realizar previsões a partir de um arquivo CSV
@app.post("/predict")
async def predict(file: UploadFile, db: Session = Depends(get_db)):
    try:
        df = pd.read_csv(file.file)  # Lê o arquivo CSV em um DataFrame do pandas
        expected_columns = ['KNR','unique_names', '1_status_10', '2_status_10', '718_status_10',
                            '1_status_13', '2_status_13', '718_status_13']  # Verifica se o arquivo contém as colunas esperadas
        if list(df.columns) != expected_columns:
            print(list(df.columns))
            raise HTTPException(status_code=400, detail=f"File must have the columns: {expected_columns}")
        
        knr = df['KNR'].iloc[0]  # Extrai o valor de KNR da primeira linha

        df = df.drop(columns=['KNR'])  # Remove a coluna KNR antes de passar os dados ao modelo

        result = call_ai(df)  # Chama a função para fazer a previsão

        for _, row in df.iterrows():  # Itera sobre cada linha do DataFrame
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
                Prediction_result=int(result),  # Armazena o resultado da previsão
                Real_result=random.randint(0, 1)  # Gera um resultado real aleatório
            )
            db.add(db_entry)  # Adiciona a entrada ao banco de dados
        db.commit()  # Confirma as alterações no banco de dados

        return {"prediction": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Rota para listar previsões salvas no banco de dados
@app.get("/predictions/")
def read_predictions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    predictions = db.query(Prediction).offset(skip).limit(limit).all()  # Retorna as previsões com paginação
    return predictions

# Rota para obter uma previsão específica pelo ID
@app.get("/prediction_id/{ID}")
def read_prediction(ID: str, db: Session = Depends(get_db)):
    prediction = db.query(Prediction).filter(Prediction.ID == ID).first()  # Busca a previsão pelo ID
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction

# Rota para atualizar uma previsão existente pelo ID
@app.put("/predictions/{ID}")
def update_prediction(ID: str, db: Session = Depends(get_db)):
    prediction = db.query(Prediction).filter(Prediction.ID == ID).first()  # Busca a previsão pelo ID
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")

    prediction.unique_names = 2.1  # Atualiza os valores dos campos
    prediction.status_10_1 = 1.234
    prediction.status_10_2 = 5.678
    prediction.Prediction_result = 1 

    db.commit()  # Confirma as alterações no banco de dados
    db.refresh(prediction)  # Recarrega o objeto atualizado
    return prediction

# Rota para deletar uma previsão pelo ID
@app.delete("/predictions/{ID}")
def delete_prediction(ID: str, db: Session = Depends(get_db)):
    prediction = db.query(Prediction).filter(Prediction.ID == ID).first()  # Busca a previsão pelo ID
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")
    db.delete(prediction)  # Remove a previsão do banco de dados
    db.commit()  # Confirma a exclusão no banco de dados
    return {"detail": "Prediction deleted"}

# Rota de healthcheck para verificar se o modelo está funcionando corretamente
@app.get("/healthcheck/model")
def healthcheck_model():
    try:
        test_prediction = 1.0  # Testa uma previsão de exemplo
        return {"status": "ok", "prediction": test_prediction}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Rota de healthcheck para verificar se o banco de dados está acessível
@app.get("/healthcheck/db")
def healthcheck_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))  # Executa uma consulta simples para verificar a conexão com o banco de dados
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Rota de healthcheck para verificar se o backend está rodando corretamente
@app.get("/healthcheck/backend")
def healthcheck_backend():
    return {"status": "ok"}