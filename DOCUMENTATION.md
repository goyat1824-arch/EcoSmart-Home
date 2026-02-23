# EcoSmart Home - Energy Intelligence & CO2 Analytics Platform

## Project Documentation

---

## 1. Problem Statement

### The Energy Crisis at Household Level

Households account for **30% of global energy consumption** and are a major contributor to carbon emissions. Yet most homeowners have **zero visibility** into:

- How much energy they consume daily and which appliances drive that consumption
- How their usage correlates with weather patterns and seasonal changes
- What their carbon footprint looks like and how it trends over time
- Whether their consumption is efficient compared to similar households
- What actionable steps they can take to reduce both cost and environmental impact

**Current pain points:**
- Electricity bills arrive monthly with no granular breakdown
- No way to predict future consumption or budget for energy costs
- No connection between energy usage and environmental impact (CO2)
- Generic energy-saving advice that isn't personalized to the household
- No data-driven decision support for appliance upgrades or behavioral changes

### What EcoSmart Home Solves

EcoSmart Home transforms raw energy meter data into **actionable intelligence** by combining:
1. **Historical analysis** - understanding past consumption patterns
2. **Machine learning prediction** - forecasting future energy needs
3. **Environmental analytics** - quantifying carbon footprint
4. **Cost intelligence** - financial impact and savings opportunities
5. **Personalized recommendations** - data-driven suggestions tailored to each household

---

## 2. How the Application Works

### 2.1 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Angular Frontend                      │
│          (Dashboard, Charts, Management UI)              │
│                   localhost:4200                          │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP REST API
┌──────────────────────▼──────────────────────────────────┐
│                  FastAPI Backend                          │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐     │
│  │  CRUD    │  │ Analytics│  │   ML Prediction    │     │
│  │  APIs    │  │ Services │  │   Engine           │     │
│  │          │  │          │  │                    │     │
│  │ Users    │  │ CO2      │  │ Feature Engineering│     │
│  │ Houses   │  │ Cost     │  │ Model Training     │     │
│  │ Appliance│  │ Score    │  │ Forecasting        │     │
│  │ Energy   │  │ Recommend│  │                    │     │
│  └────┬─────┘  └────┬─────┘  └────────┬───────────┘     │
│       │              │                 │                  │
│  ┌────▼──────────────▼─────────────────▼───────────┐     │
│  │              SQLite Database                     │     │
│  │  Users | Households | Appliances | Energy | Weather   │
│  └──────────────────────────────────────────────────┘     │
│                   localhost:8000                          │
└─────────────────────────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
┌───────▼────────┐          ┌─────────▼──────────┐
│ UCI Kaggle     │          │ Open-Meteo API     │
│ Dataset        │          │ Weather Data       │
│ 2M+ records    │          │ 2006-2010          │
│ 4 years daily  │          │ Temp/Humidity/Wind  │
└────────────────┘          └────────────────────┘
```

### 2.2 Data Pipeline

**Step 1: Data Ingestion**
- The UCI Household Electric Power Consumption dataset (2,075,259 minute-level records from a real household in Sceaux, France) is downloaded and processed
- Minute-level readings are aggregated into **1,420 daily summaries**
- Historical weather data (temperature, humidity, wind speed, precipitation) is fetched from the Open-Meteo API for the same location and date range
- Both datasets are merged and stored in SQLite

**Step 2: Feature Engineering (27 features)**
The raw data is transformed into ML-ready features:

| Category | Features | Purpose |
|----------|----------|---------|
| Temporal | day_of_week, month, day_of_year, is_weekend, season | Capture cyclical consumption patterns |
| Rolling Stats | 7-day avg, 30-day avg, 7-day std deviation | Capture recent trends and volatility |
| Lag Features | 1-day lag, 7-day lag, 14-day lag | Use past consumption to predict future |
| Weather | temp, humidity, wind_speed, precipitation | Weather drives HVAC and lighting usage |
| Derived Weather | temp_range, heating_degree_days, cooling_degree_days, temp×humidity interaction | Non-linear weather effects |
| Appliance | kitchen_kwh, laundry_kwh, hvac_kwh, hvac_ratio | Appliance-level patterns |
| Electrical | global_active_power, voltage | Grid-level indicators |

**Step 3: ML Model Training**
Three models are trained and compared using chronological 80/20 split:

| Model | MAE (kWh) | RMSE (kWh) | R² Score |
|-------|-----------|------------|----------|
| Linear Regression | 0.031 | 0.247 | **0.9989** |
| Random Forest | 0.050 | 0.252 | 0.9989 |
| XGBoost | 0.363 | 0.522 | 0.9952 |

The best model is automatically selected and saved for production use.

**Step 4: Real-time Analytics**
Every API request triggers live calculations:
- **CO2 = Energy (kWh) × Emission Factor** (configurable per country)
- **Cost = Energy (kWh) × Tariff Rate** (configurable per household)
- **Sustainability Score** = normalized comparison against baseline consumption

### 2.3 Application Modules

#### Module 1: Dashboard (Overview)
**What it shows:** A single-screen summary of the household's energy intelligence
- Today's consumption with day-over-day change percentage
- Monthly CO2 emissions and energy cost
- Sustainability score with letter grade (A+ to F)
- 7-day consumption trend chart
- Appliance category pie chart (Kitchen vs Laundry vs HVAC vs Other)
- Monthly energy + cost trend (dual-axis bar/line chart)
- Tomorrow's predicted consumption

**Problem solved:** Homeowners can instantly see their energy health at a glance instead of waiting for monthly bills.

#### Module 2: Energy History
**What it shows:** Detailed historical consumption data with filtering
- Daily consumption line chart with zoom/scroll
- Stacked bar chart showing Kitchen, Laundry, and HVAC breakdown per day
- Sortable data table with date, total kWh, per-category kWh, and peak usage hour
- Date range filtering

**Problem solved:** Users can identify patterns like "weekends use 30% more energy" or "HVAC spikes during heatwaves" and correlate consumption with specific events.

#### Module 3: ML Predictions
**What it shows:** Machine learning forecasts and model transparency
- 7-day forecast with confidence intervals (upper/lower bounds)
- Monthly total energy prediction
- Model performance comparison (MAE, RMSE, R² for all 3 models)
- Visual accuracy bars showing which model performs best

**Problem solved:** Users can plan ahead - budget for energy costs, anticipate high-consumption days, and take preventive action before peak periods.

#### Module 4: Analytics (CO2, Cost, Sustainability)
**What it shows:** Environmental and financial impact analysis
- **Sustainability Score (0-100):** Grades the household A+ to F based on efficiency vs baseline, trend improvement, and CO2 reduction
- **CO2 Emissions Chart:** Monthly carbon footprint visualization
- **Cost Analysis:** Monthly energy spending trend
- **Comparison Chart:** Energy vs Cost vs CO2 on a single multi-axis chart for correlation analysis

**Problem solved:** Makes the invisible visible - users can see the environmental cost of their energy use and track whether they're improving over time.

#### Module 5: Household & Appliance Management
**What it shows:** Inventory of the household and its connected appliances
- Household details (location, tariff rate, emission factor)
- Appliance list with wattage, daily usage hours, estimated daily kWh, and efficiency rating (1-5 stars)
- Add/delete appliances with category tagging

**Problem solved:** Users understand which appliances are the biggest energy consumers and which are inefficient (low star ratings suggest upgrade candidates).

#### Module 6: Recommendations
**What it shows:** Personalized, data-driven energy saving suggestions
- Rule-based recommendations triggered by actual consumption patterns:
  - **HVAC Optimization:** If HVAC exceeds 40% of total usage, suggests thermostat adjustments with estimated monthly savings
  - **Peak Hour Shifting:** If peak usage falls during expensive evening hours (17:00-21:00), suggests shifting to off-peak
  - **Appliance Upgrades:** Identifies low-efficiency (1-2 star) appliances and calculates ROI of upgrading to 5-star
  - **Overall Reduction:** Flags if consumption exceeds baseline (12.5 kWh/day for French household)
  - **Kitchen Optimization:** Suggests cooking efficiency improvements if kitchen exceeds 25% of total
  - **Solar Panel ROI:** Location-based solar generation estimate with payback period
- Each recommendation includes potential kWh savings and cost savings per month
- Total savings summary across all recommendations

**Problem solved:** Instead of generic "turn off lights" advice, users get personalized, quantified recommendations based on their actual data.

---

## 3. Technical Deep Dive

### 3.1 Why These Technologies?

| Technology | Choice | Reason |
|------------|--------|--------|
| Backend | **FastAPI (Python)** | Native ML library support (scikit-learn, pandas, XGBoost), automatic API documentation, async support, type validation with Pydantic |
| Frontend | **Angular 18** | Enterprise-grade framework with standalone components, lazy loading, strong typing with TypeScript, built-in HTTP client |
| Charts | **Apache ECharts** | More powerful than Chart.js - supports dual-axis, data zoom, responsive, and handles large datasets efficiently |
| Database | **SQLite** | Zero-configuration, file-based - anyone can clone and run without installing PostgreSQL/MySQL |
| ML | **scikit-learn + XGBoost** | Industry standard for tabular data prediction, easy to train/evaluate/serialize |

### 3.2 API Design

RESTful API with 20+ endpoints organized by domain:

```
/api/users/           → User management
/api/households/      → Household CRUD
/api/appliances/      → Appliance CRUD
/api/energy/          → Energy reading ingestion & retrieval
/api/analytics/       → CO2, cost, sustainability, trends
/api/predictions/     → ML forecasts & model metrics
/api/recommendations/ → Personalized suggestions
```

Full interactive documentation available at `/docs` (Swagger UI) when the backend is running.

### 3.3 ML Pipeline Design Decisions

1. **Chronological train/test split (80/20):** Unlike random splitting, this respects the time-series nature of energy data and prevents future data from leaking into training - simulating real-world deployment where the model only sees past data.

2. **27 engineered features:** Raw meter readings alone are poor predictors. Features like rolling averages capture trends, lag features capture periodicity, and weather interactions capture non-linear effects (e.g., energy spikes when both temperature AND humidity are high).

3. **Three model comparison:** Starting with Linear Regression (interpretable baseline), Random Forest (handles non-linearity), and XGBoost (state-of-the-art for tabular data). The best model is automatically selected by R² score.

4. **Confidence intervals on predictions:** Rather than point estimates, the system provides upper/lower bounds so users understand prediction uncertainty.

### 3.4 Sustainability Scoring Algorithm

```
Score = max(0, min(100, (1 - (usage_ratio - 0.5)) × 100))

Where:
  usage_ratio = household_avg_daily_kwh / baseline_daily_kwh
  baseline = 12.5 kWh/day (French household average)

Grading:
  A+ = 90-100 | A = 80-89 | B = 70-79 | C = 60-69 | D = 50-59 | F = 0-49

Trend Detection:
  Compares first half vs second half of recent 30-day readings
  - Improving: second half < 95% of first half
  - Declining: second half > 105% of first half
  - Stable: within 5% range
```

---

## 4. Real-World Impact

### For Individual Households
- **Cost savings:** Identified HVAC optimization alone can save 20% of HVAC energy
- **Carbon awareness:** Converts abstract kWh into tangible CO2 kg
- **Predictive planning:** Know tomorrow's energy bill before it happens
- **Upgrade decisions:** Data-backed ROI calculations for appliance replacements

### For Energy Providers / Smart Grid
- Demand forecasting helps grid operators plan capacity
- Peak shifting recommendations reduce grid stress during high-demand hours
- Aggregated household data could enable dynamic pricing models

### For Sustainability Goals
- Gamified sustainability scores motivate behavioral change
- CO2 tracking aligns with personal carbon footprint reduction commitments
- Solar panel ROI calculations accelerate renewable adoption

---

## 5. Dataset Details

**Source:** UCI Machine Learning Repository - Individual Household Electric Power Consumption

**Origin:** Real measurements from a single household in Sceaux, France (7km south of Paris)

**Duration:** December 2006 to November 2010 (approximately 4 years)

**Raw size:** 2,075,259 minute-level measurements → aggregated to 1,420 daily records

**Sub-metering breakdown:**
| Sub-meter | Covers | Typical Share |
|-----------|--------|---------------|
| Sub_metering_1 | Kitchen: dishwasher, oven, microwave | ~10-15% |
| Sub_metering_2 | Laundry: washing machine, dryer, refrigerator | ~15-20% |
| Sub_metering_3 | HVAC: water heater, air conditioner | ~25-35% |
| Remainder | Lighting, electronics, other circuits | ~30-40% |

**Weather data:** Open-Meteo Historical API (free, no API key required)
- Location: Sceaux, France (48.78°N, 2.29°E)
- Variables: daily avg/min/max temperature, humidity, wind speed, precipitation

---

## 6. How to Run the Application

### Prerequisites
- Python 3.11+ with pip
- Node.js 18+ with npm

### Backend (3 commands)
```bash
cd backend
pip install -r requirements.txt   # Install dependencies
python seed_data.py                # Download dataset + seed database (~2 min)
python -m app.ml.train             # Train ML models (~10 sec)
uvicorn app.main:app --reload      # Start API server → http://localhost:8000
```

### Frontend (2 commands)
```bash
cd frontend/ecosmart
npm install                        # Install dependencies
ng serve                           # Start dev server → http://localhost:4200
```

### Verification
- Backend health: `http://localhost:8000/` → returns `{"status": "healthy"}`
- API docs: `http://localhost:8000/docs` → interactive Swagger UI
- Dashboard: `http://localhost:4200` → full Angular dashboard with live data

---

## 7. Future Enhancements

| Feature | Description | Complexity |
|---------|-------------|------------|
| Real-time IoT Integration | Connect smart meters via MQTT for live data | Medium |
| LSTM Time-Series Model | Deep learning for improved long-term forecasting | High |
| Solar Generation Simulation | Estimate solar panel output based on location/weather | Medium |
| Multi-household Comparison | Benchmark against neighborhood/city averages | Low |
| Time-of-Use Tariff | Optimize for variable electricity pricing | Medium |
| EV Charging Planner | Schedule electric vehicle charging during off-peak | Medium |
| Carbon Offset Marketplace | Track and purchase carbon offsets | High |
| Mobile App | React Native or Flutter companion app | High |

---

## 8. Key Learning Outcomes

This project demonstrates proficiency in:

1. **Full-stack architecture** - Clean separation of concerns with FastAPI backend and Angular frontend communicating via REST APIs
2. **Data engineering** - Processing 2M+ raw records into clean, aggregated, ML-ready datasets
3. **Machine learning pipeline** - End-to-end: data loading → feature engineering → model training → evaluation → deployment → prediction serving
4. **Feature engineering** - 27 domain-specific features including temporal patterns, rolling statistics, weather interactions, and heating/cooling degree days
5. **Time-series best practices** - Chronological splitting, lag features, rolling windows without data leakage
6. **Domain modeling** - Translating real-world energy concepts (CO2 emissions, sustainability scoring, tariff calculations) into working software
7. **Modern frontend** - Angular standalone components, lazy-loaded routes, reactive API calls, professional data visualization with ECharts
8. **API design** - RESTful endpoints with query parameters, proper HTTP status codes, Pydantic validation, and auto-generated Swagger documentation
