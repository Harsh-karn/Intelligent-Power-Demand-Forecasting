# RULES: Working rules for this project

Section A is derived directly from the brief. Section B is working convention added for this project and is not stated in the brief.

## A. Rules from the brief
1. **Scope:** build a complete end-to-end prototype: notebook, model artifact, backend API, single-page frontend, Dockerfile, README.
2. **Granularity:** the objective is demand for every **30-minute block (48 per day)**. The data is in 10-minute intervals.
3. **Use all three data sources:** load, weather (public API, Dhanbad), and self-sourced local holidays. Do not rely on a generic national holiday calendar.
4. **Weather variables to source:** temperature, humidity, cloud cover, wind speed.
5. **Holiday list:** must cover festive **and** industrial holidays relevant to Dhanbad, Jharkhand.
6. **Clean the load data:** handle gaps, errors and outliers, and **justify the methods using EDA findings**.
7. **EDA must cover all datasets:** load, frequency, weather, holidays, with statistical **and** visual exploration.
8. **Justify the model architecture in the notebook**, with a clear, data-driven link to the EDA.
9. **Save the trained model** as an artifact and have the API **load** it.
10. **API must provide:** a fresh 24-hour forecast; weather data (temperature, humidity, cloud cover) and localized holiday data for the forecast period.
11. **Frontend:** single page; interactive forecast chart; weather visualizations; holiday markers, annotations or tables.
12. **Docker and README:** working Dockerfile; README explaining how to build and run the entire project.
13. **Submission:** single Git repository containing the notebook, backend, frontend, Dockerfile, README and the provided `Utility_consumption.csv`.

## B. Working conventions (not from the brief)
1. **No fabrication.** Facts about the data (columns, ranges, gaps, counts) come only from inspecting the actual file. Holiday dates and weather values come from a cited source. If something is unknown, record it as unknown in MEMORY.md.
2. **Cite sources** for the weather API and the holiday list in the notebook and README.
3. **Log every assumption** (for example the 48 vs 96 block question) in MEMORY.md and repeat it in the README.
4. **Do not silently drop data.** Record what was removed or imputed and why, with counts, in the notebook.
5. **Validation must respect time order.** Do not shuffle across time when splitting train and validation.
6. **Do not use information that would not exist at forecast time** as an input feature.
7. **Reproducibility:** the notebook should run top to bottom from the repository contents. The README commands must be tested from a clean clone.
8. **Keep scope minimal.** Priorities follow the scoring weights: the notebook (Milestones 1 to 3) outweighs the UI.
9. **Mark proposals vs requirements** in all project docs.
