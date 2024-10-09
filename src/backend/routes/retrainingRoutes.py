from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db
from controllers.retrainingController import retrain_model

router = APIRouter()

@router.post("/retrain")
async def retrain_endpoint(file: UploadFile, db: Session = Depends(get_db)):
    return await retrain_model(file, db)
