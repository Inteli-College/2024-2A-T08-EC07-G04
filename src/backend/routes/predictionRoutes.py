from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from controllers.predictionController import (root, mock_data, predict, read_predictions, read_prediction,
                                              update_prediction, delete_prediction)
from models.database import get_db

router = APIRouter()

router.get("/")(root)
router.post("/mock")(mock_data)
router.post("/predict")(predict)
router.get("/predictions/")(read_predictions)
router.get("/prediction_id/{ID}")(read_prediction)
router.put("/predictions/{ID}")(update_prediction)
router.delete("/predictions/{ID}")(delete_prediction)
