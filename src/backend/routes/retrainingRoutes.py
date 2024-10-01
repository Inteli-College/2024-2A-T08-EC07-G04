from fastapi import APIRouter, UploadFile, Depends
from controllers.retrainingController import retrain_model

router = APIRouter()

router.post("/models/{id_modelo}/retrain")(retrain_model)