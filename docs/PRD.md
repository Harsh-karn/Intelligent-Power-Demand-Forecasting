# PRD: Intelligent Power Demand Forecasting

**Source:** "Assignment: Intelligent Power Demand Forecasting" (Exascale Deeptech & AI Pvt. Ltd.), page 1 of the provided PDF. Everything below is taken from that brief unless marked **[Email]** (from the invitation email) or **[Open]** (not specified by the brief).

## 1. Context
- Role named in the brief: **Data Developer Intern** (the invitation email says "Data Science Intern").
- Format: described as a "high-intensity, two-week sprint". **[Email]** The deadline is **Monday 12.10.2026, 2:00 PM IST**, which is shorter than two weeks from today.
- Scenario: proof-of-concept for **Apex Power & Utilities (APU)**, "a major power provider".
- The brief tests "machine learning and web development" through "a complete, end-to-end prototype".

## 2. Objective
Predict electricity demand for **every 30-minute block of the day (48 blocks total)**, using historical data given in **10-minute intervals**. The solution must be a **scalable, container-deployable web application** with a **robust forecasting model** at its heart.

### 2.1 Inconsistency in the brief
The objective states 48 blocks of 30 minutes. The Backend section says "Generate and return a forecast for the next 24 hours (**96 blocks**)". 96 blocks in 24 hours would be 15-minute blocks, which conflicts with 30-minute blocks. **[Open]** Not resolved by the brief. See MEMORY.md.

## 3. Data inputs (the "real-world complexities" that must be incorporated)
| # | Input | What the brief says |
|---|-------|---------------------|
| 1 | Historical load: `Utility_consumption.csv` | Provided file. Timestamped load data for **several feeders**. Contains **gaps, errors and outliers** that must be handled. |
| 2 | Weather | Must be **sourced from a public API** for **Dhanbad, Jharkhand, India**. Variables: **temperature, humidity, cloud cover, wind speed**. Model performance "will depend on how effectively you integrate this external data". |
| 3 | Localized holidays | Candidate must **source** a list of **festive and industrial holidays** relevant to the **Dhanbad, Jharkhand** region. A generic national calendar "will be insufficient"; failure to account for local holidays "will negatively impact model accuracy". |

The brief says mock datasets will be provided "for some of these challenges". Only `Utility_consumption.csv` is named.

## 4. Scope: what must be built
### 4.1 Analysis and modeling (Jupyter Notebook)
1. Build and document the core forecasting model.
2. Perform a thorough EDA on all datasets (load, weather, holiday).
3. Clean `Utility_consumption.csv`: gaps, errors, outliers.
4. Source and integrate weather (public API) and the self-sourced holiday list.
5. Engineer features, select a model architecture, train, and save the artifact (e.g. `.pkl` or `.h5`).
6. Document the entire process, especially analysis and justifications, in the notebook.

### 4.2 Backend
- An API (e.g. FastAPI, Flask or Node.js/Express) that loads the saved model artifact.
- Endpoints that:
  - generate and return a forecast for the next 24 hours;
  - provide weather data (temperature, humidity, cloud cover) and localized holiday data for the forecast period, to support frontend visualizations.

### 4.3 Frontend
- Minimal **single-page** web application that calls the API.
- Interactive chart of the forecast (e.g. Chart.js, D3.js or similar).
- Visualizations or UI elements (charts, tables or annotations) for weather (temperature, humidity, cloud cover) and localized holidays for Dhanbad, Jharkhand.

### 4.4 Package
- Containerize with **Docker**.
- `README.md` with clear instructions to build and run the entire project.

## 5. Submission
A link to a **single Git repository** containing:
- Jupyter Notebook (EDA, data cleaning, feature engineering, model justification)
- Backend code
- Frontend code
- Dockerfile
- Comprehensive `README.md`
- The provided mock data file(s) (`Utility_consumption.csv`) for reproducibility

**[Email]** Alternatives: upload a `.zip`/`.rar`. A hosted prototype link (e.g. Netlify, Vercel, GitHub Pages) and screenshots are requested; a functional prototype is preferred.

## 6. Evaluation (100 points)
| Milestone | Criterion | Points |
|-----------|-----------|-------:|
| **1. EDA and cleaning (25)** | Thorough statistical and visual exploration of all datasets (load, frequency, weather, holidays) | 15 |
| | Effective cleaning of outliers/gaps, justified by EDA findings | 10 |
| **2. Features and architecture justification (35)** | Source and integrate weather and self-sourced local holiday data | 10 |
| | Thoughtful feature engineering from all data sources | 10 |
| | Clear, data-driven justification in the notebook for the modeling approach, linked to EDA | 15 |
| **3. Model and backend API (20)** | Implement and validate the model with engineered features | 10 |
| | API loads the trained model and serves a fresh 24-hour forecast | 5 |
| | API provides weather and local holiday data for the forecast period | 5 |
| **4. Frontend and deployment (20)** | Dashboard with working forecast chart plus weather and holiday visualizations | 10 |
| | Working Dockerfile and well-structured README | 10 |

## 7. Not specified by the brief **[Open]**
- Column names and schema of `Utility_consumption.csv` (file not yet inspected).
- Whether to forecast per feeder, for all feeders combined, or for a chosen feeder.
- The forecasting algorithm (the brief only says to "select a model architecture" and justify it).
- Which weather API to use ("a public API").
- Accuracy metric or target threshold.
- Required API route names and response shapes.
- Hosting platform, UI styling, and Git hosting.
