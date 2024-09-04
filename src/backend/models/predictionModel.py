from sqlalchemy import Column, String, Float, Integer
from models.database import Base

class Prediction(Base):
    __tablename__ = "table"
    ID = Column(String, primary_key=True, index=True)
    KNR = Column(String)
    unique_names = Column(Float)
    status_10_1 = Column(Float)
    status_10_2 = Column(Float)
    status_10_718 = Column(Float)
    status_13_1 = Column(Float)
    status_13_2 = Column(Float)
    status_13_718 = Column(Float)
    Prediction_result = Column(Integer)
    Real_result = Column(Integer)
