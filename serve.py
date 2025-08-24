from fastapi import FastAPI
import joblib
from pydantic import BaseModel, validator
from typing import List
import numpy as np

app = FastAPI()

# Load the trained model
model = joblib.load('model.joblib')

# Define the input data model using Pydantic
class PredictionInput(BaseModel):
    features: List[float]

    @validator('features')
    def check_features_length(cls, v):
        if len(v) != 13:
            raise ValueError('Expected 13 features')
        return v

# Define the prediction endpoint
#api route to predict heart disease
@app.post("/predict")
def predict(data: PredictionInput):
    """
    Takes a list of 13 float features and returns a prediction.
    """
    features = np.array(data.features).reshape(1, -1)
    prediction = model.predict(features)
    probability = model.predict_proba(features)

    # Decode prediction to label
    # For the heart disease dataset, 0 is 'no heart disease' and 1 is 'heart disease'
    prediction_label = "no heart disease" if prediction[0] == 0 else "heart disease"
    
    return {
        "prediction": prediction_label,
        "probability": probability.tolist()[0]
    }

@app.get("/")
def read_root():
    return {"message": "Heart Disease Prediction API"}