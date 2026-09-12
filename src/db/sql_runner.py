"""SQL Query Runner and Business Analytics Suite.

Executes and benchmarks SQL business queries against the database with safety checks,
and provides standardized ANSI SQL versions of the core business analytics queries.
"""
import time
import logging
from typing import Dict, Any, List
from sqlalchemy import text
from src.db.connection import engine

logger = logging.getLogger(__name__)

# Standard ANSI/SQLite compatible queries corresponding to core business queries in Churn.sql
CORE_BUSINESS_QUERIES = {
    "executive_kpis": """
        SELECT
            COUNT(*) AS total_customers,
            SUM(Exited) AS churned_customers,
            COUNT(*) - SUM(Exited) AS retained_customers,
            ROUND(SUM(Exited) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
            ROUND((COUNT(*) - SUM(Exited)) * 100.0 / COUNT(*), 2) AS retention_rate_pct,
            SUM(IsActiveMember) AS active_members,
            ROUND(SUM(IsActiveMember) * 100.0 / COUNT(*), 2) AS active_member_pct,
            ROUND(AVG(Age), 1) AS avg_age,
            ROUND(AVG(Balance), 2) AS avg_balance,
            ROUND(AVG(CreditScore), 1) AS avg_credit_score
        FROM churn;
    """,
    "churn_by_geography": """
        SELECT
            Geography,
            COUNT(*) AS total_customers,
            SUM(Exited) AS churned_customers,
            ROUND(SUM(Exited) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM churn), 2) AS pct_of_customer_base
        FROM churn
        GROUP BY Geography
        ORDER BY churn_rate_pct DESC;
    """,
    "churn_by_gender": """
        SELECT
            Gender,
            COUNT(*) AS total_customers,
            SUM(Exited) AS churned_customers,
            ROUND(SUM(Exited) * 100.0 / COUNT(*), 2) AS churn_rate_pct
        FROM churn
        GROUP BY Gender
        ORDER BY churn_rate_pct DESC;
    """,
    "churn_by_age_group": """
        SELECT
            AgeGroup,
            COUNT(*) AS total_customers,
            SUM(Exited) AS churned_customers,
            ROUND(SUM(Exited) * 100.0 / COUNT(*), 2) AS churn_rate_pct
        FROM churn
        GROUP BY AgeGroup
        ORDER BY 
            CASE AgeGroup
                WHEN '18-25' THEN 1
                WHEN '26-35' THEN 2
                WHEN '36-45' THEN 3
                WHEN '46-55' THEN 4
                WHEN '56-65' THEN 5
                WHEN '66+' THEN 6
                ELSE 7
            END;
    """,
    "churn_by_products": """
        SELECT
            NumOfProducts,
            COUNT(*) AS total_customers,
            SUM(Exited) AS churned_customers,
            ROUND(SUM(Exited) * 100.0 / COUNT(*), 2) AS churn_rate_pct
        FROM churn
        GROUP BY NumOfProducts
        ORDER BY NumOfProducts;
    """,
    "churn_by_activity": """
        SELECT
            CASE IsActiveMember WHEN 1 THEN 'Active' ELSE 'Inactive' END AS member_status,
            COUNT(*) AS total_customers,
            SUM(Exited) AS churned_customers,
            ROUND(SUM(Exited) * 100.0 / COUNT(*), 2) AS churn_rate_pct
        FROM churn
        GROUP BY IsActiveMember
        ORDER BY churn_rate_pct DESC;
    """,
    "high_risk_segments": """
        WITH SegmentAnalysis AS (
            SELECT
                Geography,
                AgeGroup,
                IsActiveMember,
                NumOfProducts,
                COUNT(*) AS total_customers,
                SUM(Exited) AS churned_customers,
                ROUND(SUM(Exited) * 100.0 / COUNT(*), 2) AS churn_rate_pct
            FROM churn
            GROUP BY Geography, AgeGroup, IsActiveMember, NumOfProducts
            HAVING COUNT(*) >= 20
        )
        SELECT
            Geography,
            AgeGroup,
            CASE IsActiveMember WHEN 1 THEN 'Active' ELSE 'Inactive' END AS activity,
            NumOfProducts,
            total_customers,
            churned_customers,
            churn_rate_pct,
            RANK() OVER (ORDER BY churn_rate_pct DESC) AS risk_rank
        FROM SegmentAnalysis
        ORDER BY risk_rank
        LIMIT 10;
    """
}

def execute_query(sql_query: str, params: dict = None) -> Dict[str, Any]:
    """Safely executes a read-only SQL query and returns benchmarked results."""
    # Basic SQL injection / mutation safeguard
    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "REPLACE", "CREATE"]
    tokens = [t.strip().upper() for t in sql_query.split()]
    for f in forbidden:
        if f in tokens:
            raise ValueError(f"Write operation '{f}' is prohibited in the query runner.")
    
    start_time = time.perf_counter()
    with engine.connect() as conn:
        result = conn.execute(text(sql_query), params or {})
        columns = list(result.keys()) if result.returns_rows else []
        rows = [dict(zip(columns, row)) for row in result.fetchall()] if result.returns_rows else []
    duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
    
    return {
        "columns": columns,
        "rows": rows,
        "row_count": len(rows),
        "execution_time_ms": duration_ms
    }

def run_business_query(query_key: str) -> Dict[str, Any]:
    """Executes a pre-defined named business query."""
    if query_key not in CORE_BUSINESS_QUERIES:
        raise KeyError(f"Unknown business query: {query_key}. Available: {list(CORE_BUSINESS_QUERIES.keys())}")
    return execute_query(CORE_BUSINESS_QUERIES[query_key])

if __name__ == "__main__":
    print("Testing SQL Runner with executive_kpis:")
    res = run_business_query("executive_kpis")
    print("Duration:", res["execution_time_ms"], "ms")
    print("Result:", res["rows"])
