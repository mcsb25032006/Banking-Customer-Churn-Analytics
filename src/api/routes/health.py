"""Health check and system telemetry endpoint."""
from fastapi import APIRouter
from sqlalchemy import text
from src.config import settings
from src.db.connection import engine
from src.ml.predict import get_predictor
from src.api.schemas import HealthResponse

router = APIRouter(tags=["System"])

@router.get("/health", response_model=HealthResponse)
def health_check():
    """Returns application health status, database connectivity, and loaded model version."""
    db_ok = False
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            db_ok = True
    except Exception:
        db_ok = False
        
    model_ok = False
    try:
        predictor = get_predictor()
        model_ok = predictor is not None
    except Exception:
        model_ok = False
        
    status = "healthy" if (db_ok and model_ok) else "degraded"
    
    return HealthResponse(
        status=status,
        app_name=settings.APP_NAME,
        version="1.0.0",
        model_loaded=model_ok,
        database_connected=db_ok
    )
