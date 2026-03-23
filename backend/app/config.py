from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "EcoSmart Home"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///./ecosmart.db"
    CORS_ORIGINS: list[str] = ["http://localhost:4200"]
    AUTO_SEED: bool = False

    # Default emission factors (kg CO2 per kWh)
    DEFAULT_EMISSION_FACTOR: float = 0.055  # France average
    INDIA_EMISSION_FACTOR: float = 0.82
    USA_EMISSION_FACTOR: float = 0.42
    EU_EMISSION_FACTOR: float = 0.23

    # ML model path
    MODEL_PATH: str = "trained_models/best_model.joblib"
    FEATURE_COLUMNS_PATH: str = "trained_models/feature_columns.joblib"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
