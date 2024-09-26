from datetime import datetime, timedelta
import uuid
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from models.predictionModel import Prediction
from models.database import get_db
from typing import List

def get_timestamp_from_uuid(uuid_str: str) -> datetime:
    try:
        # Extract the timestamp part from the UUID and convert it to a datetime object
        uuid_obj = uuid.UUID(uuid_str)
        timestamp = uuid_obj.time / 1e7 - 12219292800  # Convert UUID time to UNIX timestamp
        return datetime.utcfromtimestamp(timestamp)
    except ValueError:
        # Handle invalid UUID strings
        return None

def read_predictions_current_week(skip: int, limit: int, db: Session = Depends(get_db)) -> List[dict]:
    # Calculate the start of the current week (Monday at 00:00)
    today = datetime.utcnow()
    start_of_week = today - timedelta(days=today.weekday())

    # Query all records from the Prediction table
    records = db.query(Prediction).offset(skip).limit(limit).all()
    
    # Filter records that are within the current week based on the UUID timestamp
    result = []
    for record in records:
        timestamp = get_timestamp_from_uuid(record.ID)
        if timestamp and timestamp >= start_of_week:
            record_dict = record.__dict__
            record_dict.pop('_sa_instance_state', None)
            result.append(record_dict)
    
    return result
