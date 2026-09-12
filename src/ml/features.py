"""Feature engineering and transformation pipeline for Customer Churn."""
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Core column definitions
TARGET_COLUMN = "Exited"
ID_COLUMNS = ["RowNumber", "CustomerId", "Surname", "Customer_churn", "AgeGroup", "CreditScoreBand", "BalanceBand"]

RAW_NUMERIC_FEATURES = [
    "CreditScore",
    "Age",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "EstimatedSalary"
]

CATEGORICAL_FEATURES = ["Geography", "Gender"]

class BankingFeatureEngineer(BaseEstimator, TransformerMixin):
    """Custom transformer that engineers domain-specific banking churn features."""
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X_df = X.copy()
        if not isinstance(X_df, pd.DataFrame):
            X_df = pd.DataFrame(X_df)
            
        # 1. Balance to Salary ratio
        X_df["BalanceSalaryRatio"] = X_df["Balance"] / (X_df["EstimatedSalary"] + 1.0)
        
        # 2. Tenure to Age ratio (how long customer has banked relative to lifespan)
        X_df["TenureAgeRatio"] = X_df["Tenure"] / (X_df["Age"] + 1.0)
        
        # 3. Credit Score to Age ratio
        X_df["CreditScoreAgeRatio"] = X_df["CreditScore"] / (X_df["Age"] + 1.0)
        
        # 4. Products per tenure
        X_df["ProductsPerTenure"] = X_df["NumOfProducts"] / (X_df["Tenure"] + 1.0)
        
        # 5. Is zero balance indicator
        X_df["IsZeroBalance"] = (X_df["Balance"] == 0.0).astype(float)
        
        return X_df

ENGINEERED_NUMERIC_FEATURES = [
    "BalanceSalaryRatio",
    "TenureAgeRatio",
    "CreditScoreAgeRatio",
    "ProductsPerTenure",
    "IsZeroBalance"
]

ALL_NUMERIC_FEATURES = RAW_NUMERIC_FEATURES + ENGINEERED_NUMERIC_FEATURES

def create_preprocessor():
    """Creates a scikit-learn ColumnTransformer for categorical and numerical features."""
    return ColumnTransformer(
        transformers=[
            (
                "num",
                StandardScaler(),
                ALL_NUMERIC_FEATURES
            ),
            (
                "cat",
                OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False),
                CATEGORICAL_FEATURES
            )
        ],
        remainder="drop"
    )
