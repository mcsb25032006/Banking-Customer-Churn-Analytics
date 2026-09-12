"""Application configuration settings."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Banking Customer Churn Analytics Platform")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    
    # Paths
    BASE_DIR: Path = BASE_DIR
    RAW_DATA_PATH: Path = BASE_DIR / os.getenv("RAW_DATA_PATH", "Churn_Modelling.csv")
    DATA_DIR: Path = BASE_DIR / "data"
    MODELS_DIR: Path = BASE_DIR / "models"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'data' / 'churn.db'}")
    
    # ML Model Artifacts
    MODEL_PATH: Path = BASE_DIR / os.getenv("MODEL_PATH", "models/churn_model.joblib")
    METRICS_PATH: Path = BASE_DIR / os.getenv("METRICS_PATH", "models/metrics.json")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()

# Ensure directories exist
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.MODELS_DIR.mkdir(parents=True, exist_ok=True)
