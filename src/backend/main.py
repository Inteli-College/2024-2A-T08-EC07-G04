from fastapi import FastAPI, UploadFile
import pandas as pd
import torch
import torch.nn as nn

app = FastAPI()

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
async def predict(file: UploadFile):
# Step 1: Read the CSV file
    df = pd.read_csv(file.file)
    #df.drop[‘nome da coluna’]
# Step 2: Pass the DataFrame to your AI model
    result = call_ai(df)

# Step 3: Process the AI result and return a response
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
