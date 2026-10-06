# TASKS: Intelligent Power Demand Forecasting

Task list follows the brief's milestones and point weights. Items marked **(extra)** are logistics or proposals not stated in the brief.

**Deadline [Email]:** Monday 12.10.2026, 2:00 PM IST.

## 0. Setup and clarifications
- [ ] Confirm which assignment is being built (assignment 1: Power Demand Forecasting) **(extra)**
- [ ] Obtain `Utility_consumption.csv` and inspect its schema **(extra)**
- [ ] Resolve 48-block vs 96-block inconsistency (ask the company, or state the assumption in README and notebook) **(extra)**
- [ ] Create the Git repository **(extra)**

## Milestone 1: EDA and data cleaning (25 pts)
- [ ] Statistical and visual EDA of the load data, including frequency/interval checks (part of 15 pts)
- [ ] EDA of the weather data (part of 15 pts)
- [ ] EDA of the holiday data (part of 15 pts)
- [ ] Identify gaps, errors and outliers in `Utility_consumption.csv`
- [ ] Clean the load data; justify each method using EDA findings (10 pts)

## Milestone 2: Features and model justification (35 pts)
- [ ] Source weather data from a public API for Dhanbad: temperature, humidity, cloud cover, wind speed (part of 10 pts)
- [ ] Source and document the Dhanbad/Jharkhand festive and industrial holiday list, with source cited (part of 10 pts)
- [ ] Integrate weather and holidays with the load data (10 pts total with the two tasks above)
- [ ] Engineer features from all data sources (10 pts)
- [ ] Write the data-driven justification for the chosen model approach, linked to EDA (15 pts)

## Milestone 3: Model and backend API (20 pts)
- [ ] Implement and validate the model with the engineered features (10 pts)
- [ ] Save the trained model artifact (`.pkl`, `.h5` or similar)
- [ ] API: load the model and serve a fresh 24-hour forecast (5 pts)
- [ ] API: weather (temperature, humidity, cloud cover) and local holiday data for the forecast period (5 pts)

## Milestone 4: Frontend and deployment (20 pts)
- [ ] Single-page dashboard with working interactive forecast chart (part of 10 pts)
- [ ] Weather visualizations: temperature, humidity, cloud cover (part of 10 pts)
- [ ] Holiday display: markers, annotations or table (part of 10 pts)
- [ ] Working Dockerfile (part of 10 pts)
- [ ] README.md explaining how to build and run the entire project (part of 10 pts)

## Submission
- [ ] Repository contains: notebook, backend, frontend, Dockerfile, README, `Utility_consumption.csv`
- [ ] Test build and run from a clean clone **(extra)**
- [ ] **[Email]** Provide a hosted prototype link (functional prototype preferred) and screenshots
- [ ] **[Email]** Submit GitHub link or `.zip`/`.rar` before the deadline

## Proposed schedule **(extra)**
Created on Wed 07 Oct 2026, with the deadline on Mon 12 Oct at 2:00 PM IST:
| Day | Focus |
|-----|-------|
| Wed 07 – Thu 08 | Setup, EDA, cleaning, weather and holiday sourcing, features, model |
| Fri 09 | Backend API and dashboard |
| Sat 10 | Dockerfile, README, hosting |
| Sun 11 | Screenshots, clean-clone test, notebook re-run, buffer; submit |
