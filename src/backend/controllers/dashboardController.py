from datetime import datetime, timedelta
import uuid
from fastapi import HTTPException, Depends, Query
from sqlalchemy.orm import Session
from models.predictionModel import Prediction
from models.database import get_db
from typing import List, Dict, Optional

def normalize_to_current_month():
    today = datetime.utcnow()
    first_day_of_this_month = today.replace(day=1)
    last_day_of_current_month = today  # The current day will be the end of the range
    return first_day_of_this_month, last_day_of_current_month

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

def get_timestamp_from_uuid(id_str: str) -> datetime:
    try:
        # Extract the timestamp portion from the UUID (first two segments combined)
        timestamp_hex = id_str.split('-')[0] + id_str.split('-')[1]
        
        # Convert hex timestamp to milliseconds
        timestamp_ms = int(timestamp_hex, 16)
        
        # Convert milliseconds to seconds for the datetime conversion
        return datetime.utcfromtimestamp(timestamp_ms / 1000)
    except ValueError as e:
        print(f"Error parsing timestamp: {e}")
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
        print(timestamp)
        if timestamp and timestamp >= start_of_week:
            record_dict = record.__dict__
            record_dict.pop('_sa_instance_state', None)
            result.append(record_dict)
    
    return result

def read_predictions_current_day(skip: int, limit: int, db: Session = Depends(get_db)) -> List[dict]:
    # Calculate the start of the current week (Monday at 00:00)
    today = datetime.utcnow()

    # Query all records from the Prediction table
    records = db.query(Prediction).offset(skip).limit(limit).all()
    
    # Filter records that are within the current week based on the UUID timestamp
    result = []
    for record in records:
        timestamp = get_timestamp_from_uuid(record.ID)
        print(timestamp)
        if timestamp == today:
            record_dict = record.__dict__
            record_dict.pop('_sa_instance_state', None)
            result.append(record_dict)
    
    return result



def get_unique_knr_predictions_last_5_months(db: Session = Depends(get_db)) -> Dict[str, Dict[str, int]]:
    result = {}

    # Get the date ranges for the last 5 months
    ranges = get_last_5_months_ranges()

    # Query all records from the Prediction table
    records = db.query(Prediction).all()

    for i, date_range in enumerate(ranges):
        start_date = date_range["start_date"]
        end_date = date_range["end_date"]

        # Count unique KNR and prediction result for each month
        unique_knr_set = set()
        prediction_count = 0
        for record in records:
            timestamp = get_timestamp_from_uuid(record.ID)
            if timestamp and start_date <= timestamp <= end_date:
                unique_knr_set.add(record.KNR)
                if record.Prediction_result == 1:
                    prediction_count += 1
        
        result[f"mes{i+1}"] = {"carros": len(unique_knr_set), "falhas": prediction_count}

    return result  # Return the JSON-like structure


def count_unique_knr(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None)
) -> int:
    if not start_date or not end_date:
        # If start_date or end_date is not provided, use the default current month range
        start_date, end_date = normalize_to_current_month()

    # Query all records from the Prediction table
    records = db.query(Prediction).all()

    # Count the number of distinct KNR within the given date range based on the UUID timestamp
    unique_knr_set = set()
    for record in records:
        timestamp = get_timestamp_from_uuid(record.ID)
        if timestamp and start_date <= timestamp <= end_date:
            unique_knr_set.add(record.KNR)

    return len(unique_knr_set)


def count_predictions(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None)
) -> int:
    if not start_date or not end_date:
        # If start_date or end_date is not provided, use the default current month range
        start_date, end_date = normalize_to_current_month()

    # Query all records from the Prediction table
    records = db.query(Prediction).all()

    # Count how many predictions have prediction_result = 1 within the given date range
    prediction_count = 0
    for record in records:
        timestamp = get_timestamp_from_uuid(record.ID)
        if timestamp and start_date <= timestamp <= end_date and record.Prediction_result == 1:
            prediction_count += 1

    return prediction_count

def get_model_accuracy(db: Session = Depends(get_db)):
    total_predictions = db.query(Prediction).count()
    if total_predictions == 0:
        raise HTTPException(status_code=404, detail="No predictions found")
    #Calculo de positivos verdaderos
    true_positives = db.query(Prediction).filter(
        Prediction.Prediction_result == 1, 
        Prediction.Real_result == 1
    ).count()
    #Calculo de falsos negativos
    true_negatives = db.query(Prediction).filter(
        Prediction.Prediction_result == 0, 
        Prediction.Real_result == 0
    ).count()
    #Calculo da acuracia
    accuracy = (true_positives + true_negatives) / total_predictions
    return {"accuracy": accuracy}

def get_false_negatives(db: Session = Depends(get_db)):
    false_negatives_count = db.query(Prediction).filter(
        Prediction.Prediction_result == 0, 
        Prediction.Real_result == 1
    ).count()
    return {"falseNegative": false_negatives_count}