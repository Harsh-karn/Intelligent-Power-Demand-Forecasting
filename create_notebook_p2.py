import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

text1 = """\
# Phase 2: Feature Engineering & External Data Sourcing

This notebook covers the following aspects of Milestone 2:
- Sourcing weather data (temperature, humidity, cloud cover, wind speed) from a public API for Dhanbad, Jharkhand.
- Sourcing localized holiday data.
- Integrating external data with the cleaned load data to create features.
"""

code1 = """\
import pandas as pd
import requests
import numpy as np

# Load the cleaned consumption data
df_load = pd.read_csv('../Utility_consumption_cleaned.csv', parse_dates=['Datetime'], index_col='Datetime')
print(f"Loaded {df_load.shape[0]} rows. Data span: {df_load.index.min()} to {df_load.index.max()}")
"""

text2 = """\
## 2.1 Fetching Weather Data (Open-Meteo API)
We'll fetch historical hourly weather data for Dhanbad (Lat: 23.7957, Lon: 86.4304) and interpolate it to 30-minute intervals.
"""

code2 = """\
def fetch_weather_data(start_date, end_date):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": 23.7957,
        "longitude": 86.4304,
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
        "hourly": "temperature_2m,relative_humidity_2m,cloud_cover,wind_speed_10m",
        "timezone": "Asia/Kolkata"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    df_weather = pd.DataFrame(data['hourly'])
    df_weather['time'] = pd.to_datetime(df_weather['time'])
    df_weather.set_index('time', inplace=True)
    df_weather.rename(columns={
        'temperature_2m': 'Temperature',
        'relative_humidity_2m': 'Humidity',
        'cloud_cover': 'CloudCover',
        'wind_speed_10m': 'WindSpeed'
    }, inplace=True)
    
    # Resample to 30-minute and interpolate
    df_weather_30m = df_weather.resample('30min').interpolate(method='linear')
    return df_weather_30m

start_dt = df_load.index.min()
end_dt = df_load.index.max()

print("Fetching weather data...")
df_weather = fetch_weather_data(start_dt, end_dt)
print("Done. Weather data preview:")
print(df_weather.head())
"""

text3 = """\
## 2.2 Constructing the Holiday Calendar
Dhanbad is in Jharkhand, so we must include state-specific holidays like Sarhul, Chhath Puja, etc., alongside national holidays.
"""

code3 = """\
# 2017 Holidays in Jharkhand (Approximate Dates)
holidays_2017 = {
    '2017-01-26': 'Republic Day',
    '2017-02-24': 'Maha Shivaratri',
    '2017-03-13': 'Holi',
    '2017-04-04': 'Ram Navami / Sarhul',
    '2017-04-14': 'Good Friday / Ambedkar Jayanti',
    '2017-06-26': 'Eid ul-Fitr',
    '2017-08-15': 'Independence Day',
    '2017-09-02': 'Eid ul-Zuha',
    '2017-09-27': 'Durga Puja',
    '2017-09-28': 'Durga Puja',
    '2017-09-29': 'Durga Puja',
    '2017-09-30': 'Dussehra',
    '2017-10-19': 'Diwali',
    '2017-10-26': 'Chhath Puja',
    '2017-12-25': 'Christmas'
}

df_holidays = pd.DataFrame(list(holidays_2017.items()), columns=['Date', 'Holiday'])
df_holidays['Date'] = pd.to_datetime(df_holidays['Date'])
df_holidays['Is_Holiday'] = 1
print(df_holidays.head())
"""

text4 = """\
## 2.3 Merging and Feature Engineering
Now, let's merge the load, weather, and holiday data. We will also extract temporal features (hour, day of week, month).
"""

code4 = """\
# Merge Load and Weather
# The cleaned load data already has Temperature, Humidity, WindSpeed, but they are from the dataset. 
# We'll replace/augment them with the API data to ensure we have CloudCover and standardized weather.
df_merged = df_load.drop(columns=['Temperature', 'Humidity', 'WindSpeed'], errors='ignore')
df_merged = df_merged.join(df_weather, how='left')

# Add Temporal Features
df_merged['Hour'] = df_merged.index.hour
df_merged['Minute'] = df_merged.index.minute
df_merged['DayOfWeek'] = df_merged.index.dayofweek
df_merged['Month'] = df_merged.index.month
df_merged['Is_Weekend'] = df_merged['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)

# Merge Holidays
df_merged['Date_Only'] = df_merged.index.normalize()
df_merged['Datetime'] = df_merged.index
df_merged = df_merged.merge(df_holidays[['Date', 'Is_Holiday']], left_on='Date_Only', right_on='Date', how='left')
df_merged['Is_Holiday'] = df_merged['Is_Holiday'].fillna(0).astype(int)
df_merged.set_index('Datetime', inplace=True)
df_merged.drop(columns=['Date', 'Date_Only'], inplace=True)

# Final check
display(df_merged.info())
display(df_merged.head())

# Save Final Engineered Dataset
df_merged.to_csv('../Engineered_Features.csv')
print("Saved engineered dataset to 'Engineered_Features.csv'")
"""

nb['cells'] = [
    nbf.v4.new_markdown_cell(text1),
    nbf.v4.new_code_cell(code1),
    nbf.v4.new_markdown_cell(text2),
    nbf.v4.new_code_cell(code2),
    nbf.v4.new_markdown_cell(text3),
    nbf.v4.new_code_cell(code3),
    nbf.v4.new_markdown_cell(text4),
    nbf.v4.new_code_cell(code4)
]

os.makedirs('notebooks', exist_ok=True)
with open('notebooks/02_Weather_and_Holidays.ipynb', 'w') as f:
    nbf.write(nb, f)
print("Phase 2 Notebook created.")
