import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import create_tables, SessionLocal
from app.routers import users, households, appliances, energy, predictions, analytics, recommendations

logger = logging.getLogger(__name__)
settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Household Energy Intelligence & CO2 Analytics Platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables on startup and optionally seed
@app.on_event("startup")
def on_startup():
    create_tables()
    if settings.AUTO_SEED:
        from app.models.energy_reading import EnergyReading
        db = SessionLocal()
        try:
            if db.query(EnergyReading).count() == 0:
                logger.info("AUTO_SEED enabled and DB is empty — seeding data...")
                db.close()
                from seed_data import seed_database
                seed_database()
            else:
                logger.info("Database already has data, skipping seed.")
        except Exception as e:
            logger.error(f"Auto-seed failed: {e}")
        finally:
            db.close()

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(households.router, prefix="/api/households", tags=["Households"])
app.include_router(appliances.router, prefix="/api/appliances", tags=["Appliances"])
app.include_router(energy.router, prefix="/api/energy", tags=["Energy Readings"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["Predictions"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])


@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
