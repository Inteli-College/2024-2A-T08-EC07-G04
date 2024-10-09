from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from controllers.predictionController import (root, mock_data, predict, read_predictions, read_prediction,
                                              update_prediction, delete_prediction, update_model, get_knrs)
from models.database import get_db

router = APIRouter()

router.get("/")(root)
router.post("/mock")(mock_data)
router.get("/knrs/")(get_knrs)
router.post("/predict/{knr}")(predict)
router.get("/predictions/")(read_predictions)
router.get("/prediction_id/{ID}")(read_prediction)
router.patch("/predictions/{ID}")(update_prediction)
router.delete("/predictions/{ID}")(delete_prediction)
router.patch("/model/{ID}")(update_model)