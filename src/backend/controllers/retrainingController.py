from fastapi import UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
import tensorflow as tf
import os
import logging

from models.database import get_db
from models.predictionModel import Model
from utils.helpers import (authenticate_pocketbase, load_model_from_url, upload_model_to_pocketbase, generate_uuidv7, get_model_url)

logger = logging.getLogger(__name__)

async def retrain_model(file: UploadFile, id_modelo: str, db: Session = Depends(get_db)):
    try:
        token = authenticate_pocketbase()

        model_url = get_model_url(id_modelo, db)
        model = load_model_from_url(model_url)

        df = pd.read_csv(file.file)

        expected_columns = [
            'KNR',
            'unique_names',
            '1_status_10',
            '2_status_10',
            '718_status_10',
            '1_status_13',
            '2_status_13',
            '718_status_13'
        ]

        missing_columns = set(expected_columns) - set(df.columns)
        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"CSV is missing columns: {missing_columns}"
            )

        feature_columns = [
            'unique_names', '1_status_10', '2_status_10', '718_status_10', '1_status_13', '2_status_13', '718_status_13',
            '_unit_count', '%_unit_count', 'Clicks_unit_count', 'Deg_unit_count', 'Grad_unit_count', 'Nm_unit_count',
            'Unnamed:5_unit_count', 'V_unit_count', 'kg_unit_count', 'min_unit_count', 'mm_unit_count', '_unit_mean',
            '%_unit_mean', 'Clicks_unit_mean', 'Deg_unit_mean', 'Grad_unit_mean', 'Nm_unit_mean', 'Unnamed:5_unit_mean',
            'V_unit_mean', 'kg_unit_mean', 'min_unit_mean', 'mm_unit_mean'
        ]
        label_column = '718_status_13'

        X = df[feature_columns]
        y = df[label_column]

        X = X.values.astype(np.float32)
        y = y.values.astype(np.float32)

        model.fit(X, y, epochs=5, batch_size=1, validation_split=0.1)

        new_model_filename = f"model_{generate_uuidv7()}.h5"
        model_save_path = os.path.join("model", new_model_filename)

        os.makedirs("model", exist_ok=True)

        model.save(model_save_path)

        new_model_url = upload_model_to_pocketbase(model_save_path, token)

        model_record = db.query(Model).filter(Model.ID_modelo == id_modelo).first()
        if not model_record:
            raise HTTPException(status_code=404, detail="Model not found.")

        model_record.URL_modelo = new_model_url
        db.commit()
        db.refresh(model_record)

        if os.path.exists(model_save_path):
            os.remove(model_save_path)

        return {
            "detail": "Model retrained and updated successfully.",
            "model_url": new_model_url
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error during model retraining: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred during model retraining."
        )

