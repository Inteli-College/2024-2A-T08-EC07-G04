from fastapi import UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
import tensorflow as tf
import os
from models.database import get_db
from models.predictionModel import Model
from utils.helpers import (
    authenticate_pocketbase,
    load_model_from_url,
    upload_model_to_pocketbase,
    get_model_url,
    generate_uuidv7
)

pocketbase_tocken = authenticate_pocketbase()

async def retrain_model(file: UploadFile, id_modelo: str, db: Session = Depends(get_db)):
    try:
        token = authenticate_pocketbase()

        model_url = get_model_url(id_modelo, db)
        model = load_model_from_url(model_url)

        df = pd.read_csv(file.file)

        if 'label' not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'label' column.")

        X = df.drop('label', axis=1)
        y = df['label']

        X = X.values.astype(np.float32)
        y = y.values.astype(np.float32)

        model.fit(X, y, epochs=5, batch_size=32, validation_split=0.1)

        new_model_filename = f"model_{generate_uuidv7()}.h5"
        model_save_path = os.path.join("model", new_model_filename)
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

        return {"detail": "Model retrained and updated successfully.", "model_url": new_model_url}
    except HTTPException as e:
        raise e
