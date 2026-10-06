# DESIGN: Dashboard (Frontend)

Legend: **Required** = stated in the brief. **Proposed** = layout suggestion. **Open** = not decided. The brief specifies no visual style (colors, typography, branding), so none is defined here.

## 1. Requirements from the brief
- Minimal, **single-page** web application.
- Calls the backend API.
- **Interactive chart** of the forecast data (e.g. Chart.js, D3.js or similar).
- "Appropriate visualizations or UI elements (e.g., charts, tables, or annotations)" for:
  - weather: **temperature, humidity, cloud cover**;
  - localized **holiday** data for Dhanbad, Jharkhand (e.g. markers, annotations or tables).
- Scoring: 10 points for a working forecast chart plus weather and holiday visualizations.

## 2. Components
| # | Component | Data source | Status |
|---|-----------|-------------|--------|
| 1 | Forecast chart (demand vs time over the forecast period) | Forecast endpoint | Required |
| 2 | Weather visualization: temperature | Weather endpoint | Required |
| 3 | Weather visualization: humidity | Weather endpoint | Required |
| 4 | Weather visualization: cloud cover | Weather endpoint | Required |
| 5 | Holiday display: markers, annotations or table | Holiday endpoint | Required (format Open) |
| 6 | Page header with title and location (Dhanbad, Jharkhand) | Static | Proposed |
| 7 | Loading and error states for API calls | Frontend | Proposed |

## 3. Layout **(Proposed)**
```
+--------------------------------------------------------------+
| Header: Power Demand Forecast, Dhanbad, Jharkhand            |
+--------------------------------------------------------------+
| Forecast chart (interactive), holiday markers if applicable  |
+------------------------+------------------+------------------+
| Temperature chart      | Humidity chart   | Cloud cover chart|
+------------------------+------------------+------------------+
| Holiday table (holidays relevant to the forecast period)     |
+--------------------------------------------------------------+
```
The weather charts could alternatively share one chart with multiple series. **Open.**

## 4. Behavior
- On page load, call the API for forecast, weather and holiday data.
- Chart interactivity must exist (the brief says "interactive"); the specific interactions (tooltip, hover, zoom) are **Open**.
- If the forecast period contains no holiday, the holiday element should say so rather than appear empty. **(Proposed)**

## 5. Data contract
Response shapes are **Open** until the API is designed. The frontend needs at minimum:
- forecast: a time axis plus a demand value for each block;
- weather: a time axis plus temperature, humidity and cloud cover;
- holidays: date and name of each holiday in the forecast period.

Units for demand depend on the units in `Utility_consumption.csv`, which has not been inspected yet.

## 6. Open items
- Chart library choice.
- Color palette, typography and any branding (not specified by the brief).
- Whether the frontend is served by the API or separately.
