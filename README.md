# Intelligent Power Demand Forecasting

End-to-end forecasting prototype built for Apex Power & Utilities (APU) to predict electricity demand for every 30-minute block of the day using historical load data, integrated with localized weather and holiday data for Dhanbad, Jharkhand.

## Features
* **Random Forest Regressor** trained to predict 48 blocks of power consumption (24 hours).
* Handles non-linear weather relationships and specific localized holidays (e.g., Chhath Puja, Durga Puja).
* Outliers detected and interpolated via the IQR method.
* Backend served via **FastAPI**, with frontend static assets injected automatically.
* Simple and premium Single-Page Application (HTML + Tailwind CSS + Chart.js) to view the 24-hour demand forecast alongside the anticipated weather context.

## Project Structure
* `/notebooks`: Contains all 3 phases of data science work (EDA, Cleaning, Weather/Holiday Fetching, Feature Engineering, and Modeling).
* `/backend`: FastAPI service that loads the model artifact and provides endpoints for the frontend.
* `/frontend`: A sleek dashboard visualizing the `GET /forecast` data.
* `model.pkl`: The compiled machine learning artifact.

---

## 🚀 Running the Application via Docker (Recommended)

1. **Build the container:**
   ```bash
   docker build -t power-demand-forecaster .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 power-demand-forecaster
   ```

3. **View the Dashboard:**
   Open your browser and navigate to:
   **[http://localhost:8000](http://localhost:8000)**

---

## 🛠 Running the Application Locally (Without Docker)

1. **Install Dependencies:**
   Ensure you have Python 3.10+ installed.
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the FastAPI Server:**
   ```bash
   uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```

3. **View the Dashboard:**
   Open your browser and navigate to:
   **[http://localhost:8000](http://localhost:8000)**

---

## 📊 Re-running the Data Science Pipeline
If you wish to re-train the model or modify the EDA logic, you can execute the Jupyter notebooks sequentially:
1. `notebooks/01_EDA_and_Cleaning.ipynb`
2. `notebooks/02_Weather_and_Holidays.ipynb`
3. `notebooks/03_Modeling.ipynb`

This will overwrite the data outputs and the `model.pkl` in the root directory.
