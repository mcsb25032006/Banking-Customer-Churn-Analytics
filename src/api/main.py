"""FastAPI entry point for the Banking Customer Churn Analytics Platform."""
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.config import settings
from src.db.connection import engine
from src.ml.predict import get_predictor
from src.api.routes import health, predict, analytics

logging.basicConfig(level=settings.LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager to verify dependencies on application startup."""
    logger.info(f"Starting {settings.APP_NAME}...")
    # Preload predictor singleton
    try:
        predictor = get_predictor()
        logger.info(f"Predictor initialized with champion model: {predictor.model_name}")
    except Exception as e:
        logger.warning(f"Predictor preload warning (run training pipeline if missing): {e}")
    yield
    logger.info(f"Shutting down {settings.APP_NAME}...")

app = FastAPI(
    title=settings.APP_NAME,
    description="End-to-End Banking Customer Churn Analytics, SQL Query Runner & Machine Learning Microservice",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(health.router)
app.include_router(predict.router)
app.include_router(analytics.router)

# Mount static files if directory exists
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", include_in_schema=False)
def serve_dashboard():
    """Serves the interactive web analytics dashboard."""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": f"Welcome to {settings.APP_NAME}. Visit /docs for API documentation."}
