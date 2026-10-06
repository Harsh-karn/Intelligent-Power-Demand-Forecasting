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
df_load = pd.read_csv('Utility_consumption.csv')

# Display basic information and the first few rows
display(df_load.info())
display(df_load.head())
"""

text2 = """\
## 1.1 Understanding the Data and Feature Types

The dataset contains timestamps, weather variables (Temperature, Humidity, WindSpeed), and three feeders for 132KV power consumption. 
First, we'll fix the Datetime parsing and handle any trailing spaces or format issues.
"""

code2 = """\
# Convert Datetime to pandas datetime object
df_load['Datetime'] = pd.to_datetime(df_load['Datetime'], format='%d-%m-%Y %H:%M', errors='coerce')

# Check for missing datetime values
print("Missing Datetime entries:", df_load['Datetime'].isna().sum())

# Set Datetime as index
df_load.set_index('Datetime', inplace=True)
df_load.sort_index(inplace=True)

# Generate a summary of missing values
display(df_load.isnull().sum())
"""

text3 = """\
## 1.2 Addressing Gaps, Errors, and Outliers in Load Data

Let's plot the total power consumption to visually inspect the data for gaps and outliers.
"""

code3 = """\
# Calculate total power consumption across all 3 feeders
df_load['Total_PowerConsumption'] = df_load['F1_132KV_PowerConsumption'] + df_load['F2_132KV_PowerConsumption'] + df_load['F3_132KV_PowerConsumption']

# Plot the total power consumption
plt.figure(figsize=(15, 6))
plt.plot(df_load.index, df_load['Total_PowerConsumption'], alpha=0.7)
plt.title('Total 132KV Power Consumption Over Time (10-min intervals)')
plt.ylabel('Power Consumption')
plt.xlabel('Date')
plt.show()
"""

nb['cells'] = [
    nbf.v4.new_markdown_cell(text),
    nbf.v4.new_code_cell(code1),
    nbf.v4.new_markdown_cell(text2),
    nbf.v4.new_code_cell(code2),
    nbf.v4.new_markdown_cell(text3),
    nbf.v4.new_code_cell(code3)
]

os.makedirs('notebooks', exist_ok=True)
with open('notebooks/01_EDA_and_Cleaning.ipynb', 'w') as f:
    nbf.write(nb, f)
print("Notebook created.")
