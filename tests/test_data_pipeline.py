"""Tests for data loading, transformation, and database schema integrity."""
import pandas as pd
from src.config import settings
from src.db.init_db import load_and_transform_data

def test_raw_dataset_exists_and_shape():
    """Verifies raw CSV exists and contains 10,000 rows and 14 raw columns."""
    assert settings.RAW_DATA_PATH.exists()
    df = pd.read_csv(settings.RAW_DATA_PATH)
    assert df.shape[0] == 10000
    assert df.shape[1] >= 14
    assert "CustomerId" in df.columns
    assert "Exited" in df.columns

def test_data_transformation_bins():
    """Verifies analytical fields are computed without nulls."""
    df = load_and_transform_data()
    assert "AgeGroup" in df.columns
    assert "CreditScoreBand" in df.columns
    assert "BalanceBand" in df.columns
    assert "Customer_churn" in df.columns
    
    # Check no nulls in derived columns
    assert df["AgeGroup"].isnull().sum() == 0
    assert df["CreditScoreBand"].isnull().sum() == 0
    assert df["BalanceBand"].isnull().sum() == 0

def test_churn_benchmark_distribution():
    """Verifies target class churn proportion matches benchmark (20.37%)."""
    df = pd.read_csv(settings.RAW_DATA_PATH)
    churn_rate = df["Exited"].mean() * 100
    assert round(churn_rate, 2) == 20.37
