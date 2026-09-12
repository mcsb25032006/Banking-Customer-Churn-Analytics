"""Database initialization and ETL script.

Loads the raw CSV dataset, performs data cleaning, calculates analytical fields
(AgeGroup, CreditScoreBand, BalanceBand), and writes the data to the configured SQL database.
"""
import logging
import numpy as np
import pandas as pd
from sqlalchemy import text
from src.config import settings
from src.db.connection import engine

logging.basicConfig(level=settings.LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def load_and_transform_data(csv_path=None) -> pd.DataFrame:
    """Reads raw customer data and computes analytical segments."""
    path = csv_path or settings.RAW_DATA_PATH
    logger.info(f"Loading raw dataset from {path}")
    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found at {path}")
    
    df = pd.read_csv(path)
    
    # 1. Validation
    assert "CustomerId" in df.columns, "CustomerId column missing"
    assert "Exited" in df.columns, "Exited target column missing"
    
    # Check for missing values
    null_counts = df.isnull().sum()
    if null_counts.any():
        logger.warning(f"Found missing values in columns: {null_counts[null_counts > 0].to_dict()}")
    
    # 2. Compute Age Groups
    age_bins = [0, 25, 35, 45, 55, 65, 100]
    age_labels = ['18-25', '26-35', '36-45', '46-55', '56-65', '66+']
    df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, include_lowest=True).astype(str)
    
    # 3. Compute Credit Score Bands
    credit_bins = [0, 579, 669, 739, 799, 850]
    credit_labels = ['Poor', 'Fair', 'Good', 'Very Good', 'Exceptional']
    df['CreditScoreBand'] = pd.cut(df['CreditScore'], bins=credit_bins, labels=credit_labels).astype(str)
    
    # 4. Compute Balance Bands
    balance_bins = [-1, 0, 50000, 100000, 150000, 200000, np.inf]
    balance_labels = ['Zero Balance', '1-50K', '50K-100K', '100K-150K', '150K-200K', '200K+']
    df['BalanceBand'] = pd.cut(df['Balance'], bins=balance_bins, labels=balance_labels).astype(str)
    
    # 5. Customer Churn label
    df['Customer_churn'] = df['Exited'].map({0: 'Retained', 1: 'Churned'})
    
    return df

def initialize_database(csv_path=None):
    """Initializes the database schema and ingests transformed customer data."""
    df = load_and_transform_data(csv_path)
    table_name = "churn"
    
    logger.info(f"Writing {len(df)} rows to database table '{table_name}' via {engine.url}")
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)
    
    # Create indexes for optimized query performance
    with engine.connect() as conn:
        logger.info("Creating database indexes...")
        index_queries = [
            f"CREATE INDEX IF NOT EXISTS idx_churn_customer_id ON {table_name} (CustomerId)",
            f"CREATE INDEX IF NOT EXISTS idx_churn_geography ON {table_name} (Geography)",
            f"CREATE INDEX IF NOT EXISTS idx_churn_gender ON {table_name} (Gender)",
            f"CREATE INDEX IF NOT EXISTS idx_churn_exited ON {table_name} (Exited)",
            f"CREATE INDEX IF NOT EXISTS idx_churn_is_active ON {table_name} (IsActiveMember)",
            f"CREATE INDEX IF NOT EXISTS idx_churn_age_group ON {table_name} (AgeGroup)"
        ]
        for query in index_queries:
            try:
                conn.execute(text(query))
            except Exception as e:
                logger.warning(f"Index creation notice: {e}")
        conn.commit()
        
        # Verify row count
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
        logger.info(f"Database initialization complete! Verified {result} records in '{table_name}'.")
        return result

if __name__ == "__main__":
    initialize_database()
