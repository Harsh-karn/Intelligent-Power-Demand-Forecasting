# MEMORY: Project state and decision log

Update this file whenever something is learned, decided or changed. Nothing here is guessed: unknowns are listed as unknown.

## 1. Confirmed facts
**From the brief (PDF, assignment 1):**
- Company: Exascale Deeptech & AI Pvt. Ltd.; role in brief: Data Developer Intern; client scenario: Apex Power & Utilities (APU).
- Goal: forecast demand for every 30-minute block of the day (48 blocks); source data in 10-minute intervals.
- Inputs: `Utility_consumption.csv` (several feeders; gaps, errors, outliers); weather from a public API for Dhanbad, Jharkhand (temperature, humidity, cloud cover, wind speed); self-sourced festive and industrial holidays for Dhanbad/Jharkhand.
- Deliverables: notebook, backend API, frontend dashboard, Dockerfile, README, `Utility_consumption.csv` in a single Git repo.
- Scoring: M1 = 25, M2 = 35, M3 = 20, M4 = 20 (total 100).

**From the invitation email:**
- Role named in the email: Data Science Intern.
- Deadline: Monday 12.10.2026, 2:00 PM IST.
- Submit a public GitHub link or a `.zip`/`.rar`. A hosted link (Netlify, Vercel, GitHub Pages) and screenshots are requested; functional prototype preferred.

**From the user:**
- Chosen assignment: assignment 1 (Power Demand Forecasting). The PDF also contains a second brief (Carbon Emissions Reporting Platform), which is not being built.

## 2. Decisions made
| Decision | Value | Date |
|----------|-------|------|
| Assignment to build | Assignment 1: Power Demand Forecasting | 2026-10-07 |

## 3. Open questions
1. **48 vs 96 blocks.** The objective says 48 half-hour blocks per day; the Backend section says "next 24 hours (96 blocks)". Resolve or document the assumption.
2. **`Utility_consumption.csv` has not been inspected.** Column names, feeders, date range, units and missing-data patterns are unknown.
3. **Forecast target:** per feeder, aggregate, or a chosen feeder? Not specified.
4. **Mock datasets:** the brief says mock data will be provided "for some of these challenges". Only the load file is named. Confirm whether weather or holiday files were provided.
5. **Model architecture, backend framework, chart library, weather API, hosting platform:** all undecided.
6. **Evaluation metric and accuracy target:** not specified by the brief.
7. **Time available:** the brief describes a two-week sprint; the email deadline leaves less time.

## 4. Assumptions register
(none yet; add each assumption here with date and reason, and repeat it in the README)

## 5. Data notes
(empty until the CSV is inspected: row count, date range, interval, feeders, missing percentage, outlier findings)

## 6. Sources used
(empty: add the weather API and holiday list sources with URLs and retrieval dates)

## 7. Progress log
| Date | Update |
|------|--------|
| 2026-10-07 | Brief reviewed; project docs (PRD, ARCHITECTURE, RULES, DESIGN, TASKS, MEMORY) drafted from the PDF. No code written yet. |
