from fastapi import UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
import tensorflow as tf
import os
import logging

from models.database import get_db
from models.predictionModel import Model
from utils.helpers import (
    get_model_url,
    load_model_from_url,
    upload_model_to_pocketbase,
    generate_uuidv7,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def retrain_model(file: UploadFile, db: Session = Depends(get_db)):
    try:
        current_working_directory = os.getcwd()
        logger.info(f"Diretório de trabalho atual: {current_working_directory}")

        latest_model = db.query(Model).order_by(Model.ID_modelo.desc()).first()

        if not latest_model:
            raise HTTPException(status_code=404, detail="Nenhum modelo encontrado no banco de dados.")
        print(latest_model)

        model_url = str(get_model_url(latest_model.ID_modelo, db))
        print(model_url)

        model = load_model_from_url(model_url)

        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

        # Ler o arquivo CSV enviado
        df = pd.read_csv(file.file)

        expected_columns = [
            'unique_names', '1_status_10', '2_status_10', '718_status_10', '1_status_13', '2_status_13', '718_status_13',
            '_unit_count', '%_unit_count', 'Clicks_unit_count', 'Deg_unit_count', 'Grad_unit_count', 'Nm_unit_count',
            'Unnamed:5_unit_count', 'V_unit_count', 'kg_unit_count', 'min_unit_count', 'mm_unit_count', '_unit_mean',
            '%_unit_mean', 'Clicks_unit_mean', 'Deg_unit_mean', 'Grad_unit_mean', 'Nm_unit_mean', 'Unnamed:5_unit_mean',
            'V_unit_mean', 'kg_unit_mean', 'min_unit_mean', 'mm_unit_mean'
        ]

        missing_columns = set(expected_columns) - set(df.columns)
        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"CSV está faltando as colunas: {missing_columns}"
            )

        feature_columns = expected_columns.copy()
        label_column = '718_status_13'

        X = df[feature_columns].values.astype(np.float32)
        X = np.expand_dims(X, axis=1)  # Add an additional axis to make it (batch_size, timesteps, features)

        y = df[label_column].values.astype(np.float32)

        num_samples = len(X)
        validation_split = 0.1 if num_samples > 1 else 0.0

        logger.info(f"Iniciando o treinamento do modelo com {num_samples} amostras.")
        model.fit(X, y, epochs=5, batch_size=1, validation_split=validation_split)
        logger.info("Treinamento do modelo concluído.")

        id_new_model = generate_uuidv7()

        new_model_filename = f"model_{id_new_model}.h5"
        os.makedirs("model", exist_ok=True)
        model_save_path = os.path.join("model", new_model_filename)

        logger.info(f"Salvando o modelo no caminho: {model_save_path}")

        model.save(model_save_path)
        logger.info("Modelo salvo com sucesso.")

        if os.path.exists(model_save_path):
            logger.info(f"O arquivo do modelo existe em: {model_save_path}")
        else:
            logger.error(f"O arquivo do modelo NÃO foi encontrado em: {model_save_path}")
            raise HTTPException(
                status_code=500,
                detail="O arquivo do modelo não foi encontrado após salvar."
            )

        # Fazer o upload do novo modelo para o PocketBase
        new_model_url = upload_model_to_pocketbase(model_save_path)
        logger.info(f"URL do novo modelo: {new_model_url}")

        if not new_model_url:
            raise HTTPException(
                status_code=500,
                detail="Falha ao fazer upload do modelo para o PocketBase."
            )

        # Atualizar o registro do modelo no banco de dados
        model_record = Model(
            ID_modelo=id_new_model,
            model="sequencial",
            URL_modelo=new_model_url
        )
        db.add(model_record)
        db.commit()

        return {
            "detail": "Modelo retreinado e atualizado com sucesso.",
            "model_url": new_model_url
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro durante o retreinamento do modelo: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Ocorreu um erro durante o retreinamento do modelo: {str(e)}"
        )