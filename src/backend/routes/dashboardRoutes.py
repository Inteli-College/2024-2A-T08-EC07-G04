from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from controllers.dashboardController import (read_predictions_current_week, get_timestamp_from_uuid,read_predictions_current_day,count_unique_knr,count_predictions,get_unique_knr_predictions_last_5_months,get_model_accuracy,get_false_negatives)
from models.database import get_db

router = APIRouter()

router.get("/dashboard/week")(read_predictions_current_week)
router.get("/dashboard/day")(read_predictions_current_day)
router.get("/dashboard/knr_month")(count_unique_knr)
router.get("/dashboard/predictions_month")(count_predictions)
router.get("/dashboard/knr_5_months")(get_unique_knr_predictions_last_5_months)
router.get("/dashboard/accuracy")(get_model_accuracy)
router.get("/dashboard/false_negatives")(get_false_negatives)