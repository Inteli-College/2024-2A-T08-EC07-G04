from sqlalchemy import create_engine, Column, String, Float, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from models.database import Base

class Prediction(Base):
    __tablename__ = "Prediction"
    ID = Column(String, primary_key=True, index=True)
    ID_modelo = Column(String, ForeignKey('Model.ID_modelo'), index=True)
    KNR = Column(String)
    Prediction_result = Column(Integer)
    Real_result = Column(Integer)

    model = relationship('Model')
    
class Features(Base):
    __tablename__ = "features"
    ID = Column(String, ForeignKey('Prediction.ID'), primary_key=True, index=True)
    ID_modelo = Column(String, ForeignKey('Model.ID_modelo'), index=True) 
    unique_names = Column(Float)
    status_10_1 = Column(Float)
    status_10_2 = Column(Float)
    status_10_718 = Column(Float)
    status_13_1 = Column(Float)
    status_13_2 = Column(Float)
    status_13_718 = Column(Float)

    model = relationship('Model')

    features = relationship('Features', back_populates='prediction')

class Model(Base):
    __tablename__ = "Model"
    ID_modelo = Column(String, primary_key=True, index=True)
    model = Column(String)
    URL_modelo = Column(String)