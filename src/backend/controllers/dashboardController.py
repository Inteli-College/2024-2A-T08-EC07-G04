from datetime import datetime, timedelta
import uuid
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from models.predictionModel import Prediction
from models.database import get_db
from typing import List
from typing import Dict

def normalize_to_last_month():
    today = datetime.utcnow()
    first_day_of_this_month = today.replace(day=1)
    last_day_of_last_month = first_day_of_this_month - timedelta(days=1)
    first_day_of_last_month = last_day_of_last_month.replace(day=1)
    return first_day_of_last_month, last_day_of_last_month

def get_last_5_months_ranges() -> List[Dict[str, datetime]]:
    today = datetime.utcnow()
    ranges = []
    
    # Calculate the date range for each of the last 5 months
    for i in range(5):
        # Get the first day of the current month minus i months
        first_day_of_target_month = today.replace(day=1) - timedelta(days=i*30)
        # Get the last day of the target month
        last_day_of_target_month = first_day_of_target_month.replace(day=1) + timedelta(days=32)
        last_day_of_target_month = last_day_of_target_month.replace(day=1) - timedelta(days=1)
        
        ranges.append({
            "start_date": first_day_of_target_month,
            "end_date": last_day_of_target_month
        })

    return ranges

def count_unique_knr_and_prediction_result(db: Session, start_date: datetime, end_date: datetime) -> Dict[str, int]:
    # Count the number of distinct KNR within the given date range
    unique_knr_count = db.query(Prediction.KNR).filter(
        Prediction.created_at.between(start_date, end_date)
    ).distinct().count()

    # Count how many predictions have prediction_result = 1 within the given date range
    prediction_result_count = db.query(Prediction).filter(
        Prediction.prediction_result == 1,
        Prediction.created_at.between(start_date, end_date)
    ).count()

    return {"carros": unique_knr_count, "falhas": prediction_result_count}

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



def get_unique_knr_predictions_last_5_months(db: Session = Depends(get_db)) -> Dict[str, Dict[str, int]]:
    result = {}
    
    # Get the date ranges for the last 5 months
    ranges = get_last_5_months_ranges()

    for i, date_range in enumerate(ranges):
        start_date = date_range["start_date"]
        end_date = date_range["end_date"]
        
        month_data = count_unique_knr_and_prediction_result(db, start_date, end_date)
        result[f"mes{i+1}"] = month_data
    
    return result

def count_unique_knr_last_month(db: Session = Depends(get_db)):
    start_date, end_date = normalize_to_last_month()

    # Count the number of distinct KNR within the last month
    unique_count = db.query(Prediction.KNR).filter(
        Prediction.created_at.between(start_date, end_date)
    ).distinct().count()

    return {"unique_count": unique_count}

def count_predictions_last_month(db: Session = Depends(get_db)):
    start_date, end_date = normalize_to_last_month()

    # Count how many predictions have prediction_result = 1 within the last month
    count = db.query(Prediction).filter(
        Prediction.prediction_result == 1,
        Prediction.created_at.between(start_date, end_date)
    ).count()

    return {"count": count}