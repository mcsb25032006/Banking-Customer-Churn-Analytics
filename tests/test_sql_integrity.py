"""Tests for SQL query execution, window functions, and numerical correctness."""
from src.db.sql_runner import run_business_query, CORE_BUSINESS_QUERIES

def test_all_core_business_queries_execute():
    """Verifies every pre-defined analytical business query executes without syntax or runtime error."""
    for query_name in CORE_BUSINESS_QUERIES.keys():
        res = run_business_query(query_name)
        assert "rows" in res
        assert "columns" in res
        assert res["row_count"] > 0
        assert res["execution_time_ms"] >= 0

def test_geographic_churn_sql_accuracy():
    """Verifies that Germany churn rate is highest as identified in business findings."""
    res = run_business_query("churn_by_geography")
    rows = res["rows"]
    # First row ordered by churn_rate_pct DESC should be Germany
    assert rows[0]["Geography"] == "Germany"
    assert rows[0]["churn_rate_pct"] > 32.0

def test_window_function_ranking_integrity():
    """Verifies that CTE with window function RANK() produces sequential ranks starting at 1."""
    res = run_business_query("high_risk_segments")
    rows = res["rows"]
    assert len(rows) > 0
    assert rows[0]["risk_rank"] == 1
    # Ensure ranks are monotonically non-decreasing
    ranks = [r["risk_rank"] for r in rows]
    assert ranks == sorted(ranks)
