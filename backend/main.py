from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
FRONTEND_PATH = os.path.join(BASE_DIR, 'frontend')

app = FastAPI(title="Power Demand Forecasting API")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
# In production, we'd handle exceptions if the model file is missing
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    model = None

# Mock functions for fetching future weather and holidays
# In a real app, this would call an external API like Open-Meteo for a 24-hr forecast
def get_future_weather(start_time: datetime, periods=48):
    # Generating mock weather for 48 blocks (24 hours in 30-min intervals)
    timestamps = [start_time + timedelta(minutes=30*i) for i in range(periods)]
    return pd.DataFrame({
        'Datetime': timestamps,
        'Temperature': np.random.uniform(15, 35, periods),
        'Humidity': np.random.uniform(40, 90, periods),
        'CloudCover': np.random.uniform(0, 100, periods),
        'WindSpeed': np.random.uniform(0, 20, periods)
    }).set_index('Datetime')

def get_future_holidays(start_time: datetime, periods=48):
    # Mocking holiday: Assume tomorrow is a normal day
    timestamps = [start_time + timedelta(minutes=30*i) for i in range(periods)]
    return pd.DataFrame({
        'Datetime': timestamps,
        'Is_Holiday': [0] * periods
    }).set_index('Datetime')

# Root route removed since StaticFiles will serve index.html

@app.get("/forecast")
def get_forecast():
    if model is None:
        return {"error": "Model not loaded"}

    # We assume the forecast starts from "now" or a specific next day. 
    # Let's say we forecast from 2017-12-13 00:00 (the day after our dataset ends)
    start_time = datetime(2017, 12, 13, 0, 0)
    
    # 1. Get Weather & Holiday Data
    weather_df = get_future_weather(start_time, periods=48)
    holiday_df = get_future_holidays(start_time, periods=48)
    
    # 2. Prepare Features
    features_df = weather_df.copy()
    features_df['Is_Holiday'] = holiday_df['Is_Holiday']
    features_df['Hour'] = features_df.index.hour
    features_df['Minute'] = features_df.index.minute
    features_df['DayOfWeek'] = features_df.index.dayofweek
    features_df['Month'] = features_df.index.month
    features_df['Is_Weekend'] = features_df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)
    
    # Order features identically to training:
    feature_cols = ['Temperature', 'Humidity', 'CloudCover', 'WindSpeed', 
                    'Hour', 'Minute', 'DayOfWeek', 'Month', 'Is_Weekend', 'Is_Holiday']
    
    X_pred = features_df[feature_cols]
    
    # 3. Predict
    predictions = model.predict(X_pred)
    
    # 4. Format Output
    forecast_results = []
    for i, (idx, row) in enumerate(features_df.iterrows()):
        forecast_results.append({
            "timestamp": idx.strftime("%Y-%m-%d %H:%M"),
            "predicted_demand": round(predictions[i], 2),
            "temperature": round(row['Temperature'], 2),
            "humidity": round(row['Humidity'], 2),
            "cloud_cover": round(row['CloudCover'], 2)
        })
        
    return {"forecast": forecast_results}

# Mount frontend folder
app.mount("/", StaticFiles(directory=FRONTEND_PATH, html=True), name="frontend")

