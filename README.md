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

---

## Event Quiz — Energy Trivia Questions (India + App)

A collection of 55 multiple-choice questions for product demos and events. Use these to engage the audience while showcasing app features.

### General Energy Awareness — India

**Q1. What percentage of India's electricity comes from coal?**
- A) 30%
- B) 50%
- C) 70% ✅
- D) 90%

**Q2. Which Indian state consumes the most electricity?**
- A) Uttar Pradesh
- B) Maharashtra ✅
- C) Tamil Nadu
- D) Gujarat

**Q3. What is India's rank in global electricity consumption?**
- A) 1st
- B) 2nd
- C) 3rd ✅
- D) 5th

**Q4. How many hours of power cuts does rural India face on average per day?**
- A) 1–2 hours
- B) 3–4 hours ✅
- C) 6–8 hours
- D) Less than 1 hour

**Q5. What is the average monthly electricity bill for an Indian household?**
- A) ₹500–₹800
- B) ₹1,500–₹2,500 ✅
- C) ₹4,000–₹5,000
- D) ₹8,000–₹10,000

**Q6. What does "1 unit" on your electricity bill mean?**
- A) 1 Watt
- B) 1 kWh ✅
- C) 1 Megawatt
- D) 1 Volt

**Q7. How much CO₂ does India emit per year from energy production?**
- A) 500 million tonnes
- B) 1.5 billion tonnes
- C) 2.9 billion tonnes ✅
- D) 5 billion tonnes

**Q8. India's per-capita electricity consumption is how much of the global average?**
- A) About half
- B) About one-third ✅
- C) Equal to global average
- D) Double the global average

**Q9. Which ministry handles energy policy in India?**
- A) Ministry of Environment
- B) Ministry of Power ✅
- C) Ministry of Science
- D) Ministry of Finance

**Q10. What is the "Saubhagya" scheme about?**
- A) Free solar panels for farmers
- B) Free electricity connections to all households ✅
- C) Subsidized electric vehicles
- D) Smart meter installation

### Household Energy Consumption

**Q11. Which appliance in your home consumes the most electricity?**
- A) Refrigerator
- B) Washing Machine
- C) Air Conditioner ✅
- D) Television

**Q12. How much electricity does a typical 1.5-ton AC use per hour?**
- A) 0.5 kWh
- B) 1.5 kWh ✅
- C) 3 kWh
- D) 5 kWh

**Q13. What does a 5-star BEE rating mean?**
- A) Most expensive product
- B) Most energy-efficient in its category ✅
- C) Longest warranty
- D) Imported product

**Q14. How much can you save by switching from a 3-star to 5-star AC?**
- A) 5–10%
- B) 20–30% ✅
- C) 50–60%
- D) No difference

**Q15. What percentage of household electricity goes to lighting?**
- A) 5%
- B) 15–20% ✅
- C) 40%
- D) 60%

**Q16. How much energy does switching from CFL to LED save?**
- A) 10%
- B) 25%
- C) 50% ✅
- D) 80%

**Q17. How much power does a TV consume on standby mode?**
- A) 0 watts
- B) 5–15 watts ✅
- C) 50 watts
- D) 100 watts

**Q18. Which cooking method is more energy-efficient?**
- A) Gas stove (~40% efficient)
- B) Induction cooktop (~90% efficient) ✅
- C) Microwave (~30% efficient)
- D) Wood fire (~20% efficient)

**Q19. How many kWh does a refrigerator use per day?**
- A) 0.1–0.5 kWh
- B) 1–2 kWh ✅
- C) 5–6 kWh
- D) 10 kWh

**Q20. What is "phantom load" or "vampire power"?**
- A) Power surge during storms
- B) Energy consumed by devices plugged in but not in use ✅
- C) Extra power needed to start an appliance
- D) Energy lost during transmission

### Renewable Energy in India

**Q21. What is India's renewable energy target for 2030?**
- A) 100 GW
- B) 250 GW
- C) 500 GW ✅
- D) 1,000 GW

**Q22. Which Indian state leads in solar energy production?**
- A) Gujarat
- B) Rajasthan ✅
- C) Karnataka
- D) Maharashtra

**Q23. Where is the world's largest solar park located?**
- A) Ladakh, India
- B) Bhadla, Rajasthan ✅
- C) Gobi Desert, China
- D) Nevada, USA

**Q24. What percentage of India's installed capacity comes from renewables?**
- A) 10%
- B) 25%
- C) 40% ✅
- D) 60%

**Q25. Which Indian state leads in wind energy?**
- A) Rajasthan
- B) Gujarat
- C) Tamil Nadu ✅
- D) Andhra Pradesh

**Q26. How many hours of usable sunlight does India get per year?**
- A) 1,000–1,500 hours
- B) 2,500–3,000 hours ✅
- C) 4,000–5,000 hours
- D) 500–800 hours

**Q27. What is the PM-KUSUM scheme?**
- A) Free Wi-Fi for villages
- B) Solar pumps and grid-connected solar for farmers ✅
- C) Electric bus program
- D) Smart city project

**Q28. How much does a rooftop solar system cost per kW in India?**
- A) ₹10,000–₹20,000
- B) ₹50,000–₹1,00,000 ✅
- C) ₹2,00,000–₹3,00,000
- D) ₹5,00,000+

**Q29. What is the payback period of rooftop solar in India?**
- A) 1–2 years
- B) 4–6 years ✅
- C) 10–12 years
- D) 15–20 years

**Q30. What is a "net meter"?**
- A) A meter that only measures consumption
- B) A meter that measures both electricity consumed and sent back to the grid ✅
- C) A meter used only for commercial buildings
- D) A wireless smart meter

### CO₂ and Climate Change

**Q31. What is the carbon footprint of 1 kWh of coal-based electricity in India?**
- A) 0.2 kg CO₂
- B) 0.5 kg CO₂
- C) 0.82 kg CO₂ ✅
- D) 1.5 kg CO₂

**Q32. What is India's net-zero target year?**
- A) 2030
- B) 2050
- C) 2070 ✅
- D) 2100

**Q33. How many trees are needed to offset 1 tonne of CO₂ per year?**
- A) 5–10 trees
- B) 15–20 trees
- C) 40–50 trees ✅
- D) 100+ trees

**Q34. Which sector is the largest CO₂ emitter in India?**
- A) Transportation
- B) Agriculture
- C) Electricity & heat production ✅
- D) Construction

**Q35. What does "carbon footprint" mean?**
- A) Amount of carbon in the soil
- B) Total greenhouse gas emissions caused by an individual or activity ✅
- C) Weight of coal used in a factory
- D) Number of fossil fuel plants in a country

**Q36. How much CO₂ does one Indian household emit per year from electricity?**
- A) 100–200 kg
- B) 500–800 kg
- C) 1.5–2 tonnes ✅
- D) 5–10 tonnes

**Q37. What is a "sustainability score"?**
- A) A company's stock market rating
- B) A grade showing how eco-friendly your energy usage is ✅
- C) A tax on pollution
- D) A government subsidy amount

**Q38. What is the Paris Agreement's temperature goal?**
- A) Limit warming to 0.5°C
- B) Limit warming to 1.5°C ✅
- C) Limit warming to 3°C
- D) Limit warming to 5°C

**Q39. Which greenhouse gas is most responsible for global warming?**
- A) Methane
- B) Nitrous Oxide
- C) Carbon Dioxide (CO₂) ✅
- D) Ozone

**Q40. How much CO₂ can you save by using a fan instead of AC for 1 hour?**
- A) 0.1 kg
- B) 0.5 kg
- C) 1.2 kg ✅
- D) 3 kg

### App-Specific & Interactive Questions

**Q41. Can an ML model predict tomorrow's energy consumption using weather data?**
- A) No, weather has no effect
- B) Yes, and our app does exactly this! ✅
- C) Only for industrial buildings
- D) Only in winter

**Q42. Which ML model usually predicts energy consumption best?**
- A) Linear Regression
- B) Random Forest
- C) XGBoost ✅
- D) K-Nearest Neighbors

**Q43. What 3 categories does our app track in sub-metering?**
- A) Bedroom, Bathroom, Garden
- B) Kitchen, Laundry, HVAC ✅
- C) TV, Fridge, AC
- D) Solar, Wind, Grid

**Q44. How many data points were used to train our ML model?**
- A) 10,000
- B) 100,000
- C) 2 million+ ✅
- D) 50 million

**Q45. What does an R² score of 1.0 mean in a prediction model?**
- A) The model is broken
- B) The model perfectly explains the data ✅
- C) The model has 100% error
- D) The model needs more data

**Q46. What external data source improves our energy predictions?**
- A) Social media trends
- B) Stock market data
- C) Weather data (Open-Meteo API) ✅
- D) Traffic data

**Q47. How does our app calculate your electricity cost?**
- A) Fixed monthly rate
- B) kWh consumed × tariff rate (₹/kWh) ✅
- C) Number of appliances × ₹100
- D) Random estimate

**Q48. What is the formula for CO₂ from electricity?**
- A) kWh ÷ emission factor
- B) kWh × emission factor (kg CO₂/kWh) ✅
- C) Voltage × current
- D) Cost × 0.5

**Q49. How far ahead can our app forecast your energy usage?**
- A) 1 day
- B) 7 days with confidence intervals ✅
- C) 30 days
- D) 1 year

**Q50. What is a "peak hour" in energy data?**
- A) The hour when electricity is cheapest
- B) The hour of the day when your usage is highest ✅
- C) The hour when solar production peaks
- D) Midnight

### Fun / Icebreaker Bonus

**Q51. Which country generates the most solar energy in the world?**
- A) India
- B) USA
- C) China ✅
- D) Germany

**Q52. What was the first city in India to get electricity?**
- A) Mumbai
- B) Kolkata
- C) Darjeeling ✅
- D) Delhi

**Q53. How much energy does the human body produce per day?**
- A) ~10 watts
- B) ~100 watts (like a light bulb!) ✅
- C) ~500 watts
- D) ~1,000 watts

**Q54. What uses more electricity — charging your phone for a year or running AC for 1 day?**
- A) Charging phone for a year
- B) Running AC for 1 day ✅
- C) They're about the same
- D) Neither uses much

**Q55. If every Indian switched off one light for 1 hour, how much energy would we save?**
- A) Enough to charge 1,000 phones
- B) Enough to power a small city ✅
- C) Almost nothing
- D) Enough to power the entire country

### Event Tips

- **Easy round**: Q6, Q11, Q20, Q35, Q52 (warm up the crowd)
- **During demo**: Q41–Q50 (tie each question to a feature you're showing)
- **Challenge round**: Q7, Q31, Q44, Q45 (for the nerdy audience)
- **Fun closer**: Q53, Q54, Q55 (end on a high note)
