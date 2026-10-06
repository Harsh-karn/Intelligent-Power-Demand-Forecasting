import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

text1 = """\
# Phase 3: Model Architecture Justification & Training

This notebook covers the following aspects of Milestone 2 and 3:
- Data-driven justification for the chosen modeling approach based on EDA.
- Implementing and validating the proposed model using the engineered features.
- Saving the trained model artifact for the backend API.
"""

code1 = """\
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
from IPython.display import display

# Load the engineered dataset
df = pd.read_csv('../Engineered_Features.csv', parse_dates=['Datetime'], index_col='Datetime')
print(f"Dataset shape: {df.shape}")
display(df.head())
"""

text2 = """\
## 3.1 Model Architecture Justification

Based on the Exploratory Data Analysis, the power demand exhibits:
1. **Strong non-linear patterns**: Daily cycles (peak/off-peak hours) and seasonal weather impacts.
2. **Categorical influences**: Weekends and specific local holidays (e.g., Chhath Puja, Durga Puja) cause sharp deviations from normal patterns.
3. **Weather correlation**: Temperature and humidity have complex, non-linear relationships with power demand (e.g., high demand during both very cold and very hot periods).

**Chosen Model: Random Forest Regressor**
- **Why**: Random Forests excel at capturing complex, non-linear interactions without requiring extensive scaling or normalization of features. They naturally handle categorical-like integer features (Hour, DayOfWeek, Month) and are highly robust to outliers that might still exist in the data. They also provide feature importance out-of-the-box.
- **Alternative considered**: ARIMA/SARIMA are excellent for linear time series but struggle with external regressors like specific localized holidays and complex weather interactions without manual feature engineering. Deep Learning (LSTMs) requires significantly more data and tuning.
"""

code2 = """\
# Prepare Features (X) and Target (y)
# We want to predict Total_PowerConsumption. 
# We'll drop individual feeder consumption as they sum up to our target.
features = ['Temperature', 'Humidity', 'CloudCover', 'WindSpeed', 
            'Hour', 'Minute', 'DayOfWeek', 'Month', 'Is_Weekend', 'Is_Holiday']
target = 'Total_PowerConsumption'

X = df[features]
y = df[target]

# Drop any remaining NaNs
X = X.dropna()
y = y.loc[X.index]

# Time-based train-test split (Last 30 days for testing)
split_idx = int(len(X) * 0.9)
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

print(f"Training set: {X_train.shape[0]} samples")
print(f"Testing set: {X_test.shape[0]} samples")
"""

text3 = """\
## 3.2 Model Training and Validation
We'll train the Random Forest Regressor and evaluate it on the holdout test set using MAE and RMSE.
"""

code3 = """\
# Initialize and train the model
rf_model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)

# Predictions
y_pred = rf_model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")
"""

text4 = """\
## 3.3 Visualizing Predictions vs Actuals
Let's visualize how our model performs on a 3-day slice of the test set.
"""

code4 = """\
plt.figure(figsize=(15, 6))
# Plot first 144 blocks (3 days * 48 blocks)
plot_slice = 144
plt.plot(y_test.index[:plot_slice], y_test.values[:plot_slice], label='Actual Demand', alpha=0.8)
plt.plot(y_test.index[:plot_slice], y_pred[:plot_slice], label='Predicted Demand', alpha=0.8, linestyle='--')
plt.title('Actual vs Predicted Power Demand (First 3 Days of Test Set)')
plt.ylabel('Power Consumption')
plt.xlabel('Date')
plt.legend()
plt.show()

# Feature Importance
importances = rf_model.feature_importances_
indices = np.argsort(importances)

plt.figure(figsize=(10, 6))
plt.title('Feature Importances')
plt.barh(range(len(indices)), importances[indices], align='center')
plt.yticks(range(len(indices)), [features[i] for i in indices])
plt.xlabel('Relative Importance')
plt.show()
"""

text5 = """\
## 3.4 Saving the Model Artifact
We will export the trained model to a `.pkl` file so that the FastAPI backend can load it and serve predictions.
"""

code5 = """\
# Save the model
model_path = '../model.pkl'
joblib.dump(rf_model, model_path)
print(f"Model successfully saved to {model_path}")
"""

nb['cells'] = [
    nbf.v4.new_markdown_cell(text1),
    nbf.v4.new_code_cell(code1),
    nbf.v4.new_markdown_cell(text2),
    nbf.v4.new_code_cell(code2),
    nbf.v4.new_markdown_cell(text3),
    nbf.v4.new_code_cell(code3),
    nbf.v4.new_markdown_cell(text4),
    nbf.v4.new_code_cell(code4),
    nbf.v4.new_markdown_cell(text5),
    nbf.v4.new_code_cell(code5)
]

os.makedirs('notebooks', exist_ok=True)
with open('notebooks/03_Modeling.ipynb', 'w') as f:
    nbf.write(nb, f)
print("Phase 3 Notebook created.")
