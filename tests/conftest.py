"""Pytest fixtures and configuration."""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.ml.predict import get_predictor

@pytest.fixture(scope="session")
def client():
    """FastAPI TestClient session fixture."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="session")
def predictor():
    """Trained churn predictor singleton fixture."""
    return get_predictor()

@pytest.fixture
def sample_customer_high_risk():
    return {
        "CreditScore": 620,
        "Geography": "Germany",
        "Gender": "Female",
        "Age": 52,
        "Tenure": 3,
        "Balance": 125000.0,
        "NumOfProducts": 1,
        "HasCrCard": 1,
        "IsActiveMember": 0,
        "EstimatedSalary": 95000.0
    }

@pytest.fixture
def sample_customer_low_risk():
    return {
        "CreditScore": 750,
        "Geography": "France",
        "Gender": "Male",
        "Age": 28,
        "Tenure": 6,
        "Balance": 0.0,
        "NumOfProducts": 2,
        "HasCrCard": 1,
        "IsActiveMember": 1,
        "EstimatedSalary": 60000.0
    }
