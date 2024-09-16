from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, Depends
from models.database import get_db

def healthcheck_model():
    try:
        test_prediction = 1.0
        return {"status": "ok", "prediction": test_prediction}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def healthcheck_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def healthcheck_backend():
    return {"status": "ok"}
