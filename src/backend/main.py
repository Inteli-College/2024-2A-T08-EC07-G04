from fastapi import FastAPI, UploadFile, Depends
import pandas as pd
import torch
import torch.nn as nn
from sqlalchemy import create_engine, Column, Integer, String , Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "postgresql://postgres:SENHA@localhost:5432/fillmore"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define a SQLAlchemy model to save the data
class Prediction(Base):

    # Please change all of this with the actual structure of the database
    __tablename__ = "prediction_data"

    KNR = Column(String)
    feature1 = Column(String)
    feature2 = Column(Float)
    feature3 = Column(Float)
    # Add all your features here...
    prediction_result = Column(Float)

# Create the table in the database
Base.metadata.create_all(bind=engine)


app = FastAPI()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        # This is just an example. Please change it to what matches your model
        self.fc1 = nn.Linear(10, 50)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(50, 20)
        self.fc3 = nn.Linear(20, 1)

    def forward(self, x):
        # Just another example again. Please change it
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        return x  # Replace with your forward pass logic

model = MyModel()
model.eval()

def call_ai(df: pd.DataFrame):
    # Step 1: Convert the DataFrame to a tensor
    # Assuming df has the required 10 features
    input_tensor = torch.tensor(df.values, dtype=torch.float32)

    # Step 2: Ensure the input tensor has the correct shape
    if input_tensor.ndimension() == 1:
        input_tensor = input_tensor.unsqueeze(0)  # Add batch dimension if needed

    # Step 3: Get the prediction
    with torch.no_grad():  # Disable gradient calculations for inference
        prediction = model(input_tensor)

    # Step 4: Return the prediction as a scalar
    return prediction.item()

@app.get("/")
async def root():
    return {"message": "Hello World"}



#-Caso não divida em 2 modelos
@app.post("/predict")
async def predict(file: UploadFile, db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    result = call_ai(df)

    # Save the data and prediction to the database
    for _, row in df.iterrows():
        db_entry = Prediction(
            feature1=row[0],  # Replace with your actual column mappings
            feature2=row[1],
            feature3=row[2],
            # Continue for all features
            prediction_result=result
        )
        db.add(db_entry)
    db.commit()

    return {"prediction": result}

#-Caso a gente divida em 2 modelos
# @app.post("/predict_binary")
# async def predict_binary (file: UploadFile):
# 	df = pd.read_csv(file.file)
# 	result = call_ai_binary(df)
# 	if result is False:
# 		return {"prediction": result}
# 	if result:
# 		result = call_ai_fail(df)
# 		return {"prediction": result}
