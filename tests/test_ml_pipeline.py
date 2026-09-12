"""Tests for machine learning feature engineering, model inference, and explainability."""
import pandas as pd
from src.config import settings
from src.ml.features import BankingFeatureEngineer
from src.ml.predict import get_predictor

def test_model_artifact_exists():
    """Verifies that serialized champion model artifact exists."""
    assert settings.MODEL_PATH.exists()
    assert settings.METRICS_PATH.exists()

def test_feature_engineering_transformer():
    """Verifies that BankingFeatureEngineer produces interaction features."""
    sample_df = pd.DataFrame([{
        "Balance": 100000.0,
        "EstimatedSalary": 50000.0,
        "Tenure": 4,
        "Age": 40,
        "CreditScore": 600,
        "NumOfProducts": 2
    }])
    transformer = BankingFeatureEngineer()
    transformed = transformer.transform(sample_df)
    
    assert "BalanceSalaryRatio" in transformed.columns
    assert "TenureAgeRatio" in transformed.columns
    assert "CreditScoreAgeRatio" in transformed.columns
    assert "ProductsPerTenure" in transformed.columns
    assert "IsZeroBalance" in transformed.columns
    assert transformed["IsZeroBalance"].iloc[0] == 0.0

def test_single_prediction_high_risk(predictor, sample_customer_high_risk):
    """Verifies that a high-risk customer profile is correctly classified with risk factors."""
    res = predictor.predict_single(sample_customer_high_risk)
    assert res["churn_probability"] >= 0.55
    assert res["risk_tier"] == "High"
    assert res["predicted_churn"] is True
    assert len(res["primary_risk_factors"]) > 0
    assert "retention_strategy" in res
    assert len(res["retention_strategy"]["actionable_steps"]) >= 2

def test_single_prediction_low_risk(predictor, sample_customer_low_risk):
    """Verifies that a low-risk customer profile receives a low probability score."""
    res = predictor.predict_single(sample_customer_low_risk)
    assert res["churn_probability"] < 0.25
    assert res["risk_tier"] == "Low"
    assert res["predicted_churn"] is False

def test_batch_prediction(predictor, sample_customer_high_risk, sample_customer_low_risk):
    """Verifies batch inference processing."""
    batch_df = pd.DataFrame([sample_customer_high_risk, sample_customer_low_risk])
    scored_df = predictor.predict_batch(batch_df)
    
    assert "churn_probability" in scored_df.columns
    assert "predicted_churn" in scored_df.columns
    assert "risk_tier" in scored_df.columns
    assert len(scored_df) == 2
