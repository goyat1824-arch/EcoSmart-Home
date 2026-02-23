# EcoSmart Home - Energy Intelligence & CO2 Analytics Platform

A full-stack Household Energy Intelligence Platform that combines **data engineering**, **ML prediction**, **sustainability analytics**, and **interactive dashboard visualization**.

## Architecture

```
Backend:  Python FastAPI + SQLAlchemy (SQLite) + scikit-learn/XGBoost
Frontend: Angular 18 + Apache ECharts
Dataset:  UCI Household Electric Power Consumption (2M+ records, 4 years)
Weather:  Open-Meteo Historical API
```

## Features

| Module | Description |
|--------|-------------|
| Dashboard | Real-time overview with stat cards, charts, predictions |
| Energy History | Daily consumption tracking with date filters and data tables |
| Predictions | ML-powered 7-day/monthly forecasts with confidence intervals |
| Analytics | CO2 emissions, cost analysis, sustainability scoring (A-F grades) |
| Households | Household & appliance management with CRUD operations |
| Recommendations | Personalized energy-saving suggestions with savings estimates |

## ML Pipeline

- **Feature Engineering**: 27 features including rolling averages, lag features, weather interactions, heating/cooling degree days
- **Models Trained**: Linear Regression, Random Forest, XGBoost
- **Best Model Selection**: Automatic based on R² score
- **Chronological Split**: 80/20 to prevent data leakage

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm 9+

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Seed database (downloads UCI dataset + weather data)
python seed_data.py

# Train ML model
python -m app.ml.train

# Start API server
uvicorn app.main:app --reload
```

API will be available at `http://localhost:8000`
Swagger docs at `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend/ecosmart

# Install dependencies
npm install

# Start dev server
ng serve
```

Dashboard will be available at `http://localhost:4200`

## API Endpoints

### CRUD
- `POST/GET /api/users/` - User management
- `POST/GET/PUT/DELETE /api/households/` - Household management
- `POST/GET/PUT/DELETE /api/appliances/` - Appliance management
- `POST/GET /api/energy/` - Energy readings

### Analytics
- `GET /api/analytics/summary` - Dashboard summary
- `GET /api/analytics/co2` - CO2 emission data
- `GET /api/analytics/cost` - Cost analysis
- `GET /api/analytics/sustainability-score` - Sustainability grading
- `GET /api/analytics/monthly-trend` - Monthly aggregated trends
- `GET /api/analytics/appliance-breakdown` - Usage by category

### Predictions
- `GET /api/predictions/daily` - N-day forecast
- `GET /api/predictions/monthly` - Monthly forecast
- `GET /api/predictions/model-metrics` - Model performance metrics

### Recommendations
- `GET /api/recommendations/` - Personalized suggestions

## Dataset

**UCI Household Electric Power Consumption** - 2,075,259 minute-level measurements from a house in Sceaux, France (Dec 2006 - Nov 2010).

Sub-metering breakdown:
- Sub_metering_1: Kitchen (dishwasher, oven, microwave)
- Sub_metering_2: Laundry (washing machine, dryer, refrigerator)
- Sub_metering_3: HVAC (water heater, air conditioner)

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, Pandas, scikit-learn, XGBoost
- **Frontend**: Angular 18, Apache ECharts, SCSS
- **Database**: SQLite
- **Weather API**: Open-Meteo (free, no API key)
