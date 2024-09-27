from sqlalchemy import create_engine, Column, String, Float, Integer, ForeignKey, PrimaryKeyConstraint
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
    values = relationship('Values', back_populates='prediction')

class Features(Base):
    __tablename__ = "Features"
    ID_feature = Column(Integer, primary_key=True)
    name_feature = Column(String)

class Model(Base):
    __tablename__ = "Model"
    ID_modelo = Column(String, primary_key=True, index=True)
    model = Column(String)
    URL_modelo = Column(String)
    precision = Column(Float)
    # features = Column(ARRAY(Integer))
    

class Values(Base):
    __tablename__ = "Values"
    ID_feature = Column(Integer, ForeignKey('Features.ID_feature'), index=True)
    ID = Column(String, ForeignKey('Prediction.ID'), index=True)
    ID_modelo = Column(String, ForeignKey('Model.ID_modelo'), index=True)
    value_feature = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint('ID_feature', 'ID', 'ID_modelo'),
    )

    feature = relationship('Features')
    model = relationship('Model')
    prediction = relationship('Prediction', back_populates='values')