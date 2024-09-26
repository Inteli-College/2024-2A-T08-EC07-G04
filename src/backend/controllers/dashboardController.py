from datetime import datetime, timedelta
import uuid
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from models.predictionModel import Prediction, Features, Model, Values
from models.database import get_db
from typing import List

def get_timestamp_from_uuid(uuid_str: str) -> datetime:
    # Extract the timestamp part from the UUID and convert it to a datetime object
    # Assuming the timestamp is in the first part of the UUID
    uuid_obj = uuid.UUID(uuid_str)
    timestamp = uuid_obj.time / 1e7 - 12219292800  # Convert UUID time to UNIX timestamp
    return datetime.utcfromtimestamp(timestamp)

def read_predictions_last_month(table: str, skip: int, limit: int, db: Session = Depends(get_db)) -> List[dict]:
    table_map = {
        'Prediction': Prediction,
        'Features': Features,
        'Model': Model,
        'Values': Values
    }
    
    if table not in table_map:
        raise HTTPException(status_code=400, detail=f"Table '{table}' not recognized.")
    
    model_class = table_map[table]

    # Calculate the date for one month ago
    one_month_ago = datetime.utcnow() - timedelta(days=30)

    # Query all records from the database
    records = db.query(model_class).offset(skip).limit(limit).all()
    
    # Filter records that are within the last month based on the UUID timestamp
    result = [
        record.__dict__ for record in records 
        if get_timestamp_from_uuid(record.ID) >= one_month_ago
    ]
    
    for record in result:
        record.pop('_sa_instance_state', None)
    
    return result
