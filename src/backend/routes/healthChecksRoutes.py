from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.healthCheckController import healthcheck_model, healthcheck_db, healthcheck_backend
from models.database import get_db

router = APIRouter()

router.get("/healthcheck/model")(healthcheck_model)
router.get("/healthcheck/db")(healthcheck_db)
router.get("/healthcheck/backend")(healthcheck_backend)
