"""Prediction endpoints for real-time customer churn inference."""
import json
from fastapi import APIRouter, HTTPException, status
from src.config import settings
from src.ml.predict import get_predictor
from src.api.schemas import (
    CustomerInput,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse
)

router = APIRouter(prefix="/api/v1/predict", tags=["Prediction"])

@router.post("", response_model=PredictionResponse, status_code=status.HTTP_200_OK)
def predict_churn(customer: CustomerInput):
    """Computes real-time churn probability, risk tier, drivers, and retention recommendations."""
    try:
        predictor = get_predictor()
        res = predictor.predict_single(customer.model_dump())
        return PredictionResponse(**res)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error: {str(e)}"
        )

@router.post("/batch", response_model=BatchPredictionResponse, status_code=status.HTTP_200_OK)
def predict_batch_churn(batch: BatchPredictionRequest):
    """Scores a batch of customer profiles (up to 1,000 customers)."""
    try:
        predictor = get_predictor()
        predictions = []
        high_count = 0
        med_count = 0
        low_count = 0
        
        for c in batch.customers:
            pred = predictor.predict_single(c.model_dump())
            predictions.append(PredictionResponse(**pred))
            if pred["risk_tier"] == "High":
                high_count += 1
            elif pred["risk_tier"] == "Medium":
                med_count += 1
            else:
                low_count += 1
                
        return BatchPredictionResponse(
            total_scored=len(predictions),
            high_risk_count=high_count,
            medium_risk_count=med_count,
            low_risk_count=low_count,
            predictions=predictions
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch inference error: {str(e)}"
        )

@router.get("/metrics")
def get_model_evaluation_metrics():
    """Returns champion model metrics, cross-validation scores, and feature importances."""
    if not settings.METRICS_PATH.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model evaluation metrics artifact not found."
        )
    with open(settings.METRICS_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)
    return metrics
