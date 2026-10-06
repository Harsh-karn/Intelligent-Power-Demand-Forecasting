import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

text = """\
# Phase 1: Exploratory Data Analysis (EDA) & Data Cleaning

This notebook covers the following aspects of Milestone 1:
- Conducts a thorough statistical and visual exploration of all datasets (load, frequency, weather, holidays) to uncover insights.
- Effectively cleans the load data and handles outliers/gaps, justifying the methods based on your EDA findings.

Let's start by importing necessary libraries and loading the `Utility_consumption.csv`.
"""

code1 = """\
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configure plot style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Load the historical load data
df_load = pd.read_csv('../Utility_consumption.csv')

# Display basic information and the first few rows
display(df_load.info())
display(df_load.head())
"""

text2 = """\
## 1.1 Understanding the Data and Feature Types

The dataset contains timestamps, weather variables (Temperature, Humidity, WindSpeed), and three feeders for 132KV power consumption. 
Notice that the Datetime format switches midway through the dataset (from `DD-MM-YYYY HH:MM` to `M/D/YYYY H:MM`). We will parse these robustly.
"""

code2 = """\
# Parse mixed datetime formats
df_load['Datetime'] = pd.to_datetime(df_load['Datetime'], format='mixed', dayfirst=True)

# Set Datetime as index
df_load.set_index('Datetime', inplace=True)
df_load.sort_index(inplace=True)

# Generate a summary of missing values
print("Missing values per column:\\n", df_load.isnull().sum())
"""

text3 = """\
## 1.2 Resampling to 30-Minute Blocks

The core objective requires forecasting for 30-minute blocks. The raw data is at 10-minute intervals. We will resample this down to 30 minutes. We can use the mean for temperature, humidity, windspeed, and power consumption.
"""

code3 = """\
# Resample to 30-minute intervals using the mean
df_30m = df_load.resample('30min').mean()

print(f"Data shape after resampling: {df_30m.shape}")
display(df_30m.head())
"""

text4 = """\
## 1.3 Addressing Gaps, Errors, and Outliers in Load Data

Let's plot the total power consumption to visually inspect the data for gaps and outliers.
"""

code4 = """\
# Calculate total power consumption across all 3 feeders
df_30m['Total_PowerConsumption'] = df_30m['F1_132KV_PowerConsumption'] + df_30m['F2_132KV_PowerConsumption'] + df_30m['F3_132KV_PowerConsumption']

# Plot the total power consumption
plt.figure(figsize=(15, 6))
plt.plot(df_30m.index, df_30m['Total_PowerConsumption'], alpha=0.7)
plt.title('Total 132KV Power Consumption Over Time (30-min intervals)')
plt.ylabel('Power Consumption')
plt.xlabel('Date')
plt.show()
"""

text5 = """\
### Outlier Detection and Treatment
We will identify outliers using the Interquartile Range (IQR) method on the total power consumption and then interpolate missing or extreme values.
"""

code5 = """\
# Detect Outliers using IQR
Q1 = df_30m['Total_PowerConsumption'].quantile(0.25)
Q3 = df_30m['Total_PowerConsumption'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Mark outliers as NaN so we can interpolate them along with actual missing gaps
outliers_mask = (df_30m['Total_PowerConsumption'] < lower_bound) | (df_30m['Total_PowerConsumption'] > upper_bound)
print(f"Number of outliers detected: {outliers_mask.sum()}")

df_clean = df_30m.copy()
df_clean.loc[outliers_mask, :] = np.nan

# Interpolate missing values (using time-based interpolation)
df_clean = df_clean.interpolate(method='time')

# Plot the cleaned data
plt.figure(figsize=(15, 6))
plt.plot(df_clean.index, df_clean['Total_PowerConsumption'], alpha=0.7, color='green')
plt.title('Cleaned Total 132KV Power Consumption')
plt.ylabel('Power Consumption')
plt.xlabel('Date')
plt.show()
"""

text6 = """\
## 1.4 Saving the Cleaned Data
We will save this cleaned 30-minute block dataset so it can be merged with weather and holiday data in the next phase.
"""

code6 = """\
# Save the cleaned dataframe
df_clean.to_csv('../Utility_consumption_cleaned.csv')
print("Cleaned data saved to 'Utility_consumption_cleaned.csv'")
"""

nb['cells'] = [
    nbf.v4.new_markdown_cell(text),
    nbf.v4.new_code_cell(code1),
    nbf.v4.new_markdown_cell(text2),
    nbf.v4.new_code_cell(code2),
    nbf.v4.new_markdown_cell(text3),
    nbf.v4.new_code_cell(code3),
    nbf.v4.new_markdown_cell(text4),
    nbf.v4.new_code_cell(code4),
    nbf.v4.new_markdown_cell(text5),
    nbf.v4.new_code_cell(code5),
    nbf.v4.new_markdown_cell(text6),
    nbf.v4.new_code_cell(code6)
]

os.makedirs('notebooks', exist_ok=True)
with open('notebooks/01_EDA_and_Cleaning.ipynb', 'w') as f:
    nbf.write(nb, f)
print("Updated Notebook created.")
