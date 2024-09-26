from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from controllers.dashboardController import (read_predictions_current_week, get_timestamp_from_uuid)
from models.database import get_db

router = APIRouter()

router.get("/dashboard/week")(read_predictions_current_week)