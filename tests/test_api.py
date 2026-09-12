"""End-to-end integration tests for FastAPI routes and API validation."""
import pytest

def test_health_endpoint(client):
    """Verifies that system health telemetry endpoint is operational."""
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert data["database_connected"] is True

def test_root_serves_html(client):
    """Verifies that root URL serves the interactive web dashboard."""
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Banking Churn Analytics" in resp.text

def test_predict_endpoint_valid_input(client, sample_customer_high_risk):
    """Verifies successful churn prediction on valid customer payload."""
    resp = client.post("/api/v1/predict", json=sample_customer_high_risk)
    assert resp.status_code == 200
    data = resp.json()
    assert "churn_probability" in data
    assert "churn_probability_pct" in data
    assert "risk_tier" in data
    assert "primary_risk_factors" in data
    assert "retention_strategy" in data
    assert data["risk_tier"] == "High"

def test_predict_endpoint_validation_errors(client, sample_customer_high_risk):
    """Verifies strict Pydantic validation rejects out-of-range inputs."""
    # 1. Invalid credit score > 850
    bad_credit = sample_customer_high_risk.copy()
    bad_credit["CreditScore"] = 999
    assert client.post("/api/v1/predict", json=bad_credit).status_code == 422
    
    # 2. Invalid age < 18
    bad_age = sample_customer_high_risk.copy()
    bad_age["Age"] = 15
    assert client.post("/api/v1/predict", json=bad_age).status_code == 422
    
    # 3. Invalid country not in Literal
    bad_geo = sample_customer_high_risk.copy()
    bad_geo["Geography"] = "Brazil"
    assert client.post("/api/v1/predict", json=bad_geo).status_code == 422

def test_batch_predict_endpoint(client, sample_customer_high_risk, sample_customer_low_risk):
    """Verifies batch scoring endpoint."""
    payload = {"customers": [sample_customer_high_risk, sample_customer_low_risk]}
    resp = client.post("/api/v1/predict/batch", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_scored"] == 2
    assert len(data["predictions"]) == 2

def test_metrics_endpoint(client):
    """Verifies model metrics retrieval endpoint."""
    resp = client.get("/api/v1/predict/metrics")
    assert resp.status_code == 200
    data = resp.json()
    assert "champion_model" in data
    assert "benchmark_comparison" in data
    assert "feature_importances" in data

def test_analytics_kpis_endpoint(client):
    """Verifies executive KPIs endpoint returns accurate business metrics."""
    resp = client.get("/api/v1/analytics/kpis")
    assert resp.status_code == 200
    kpis = resp.json()["kpis"]
    assert kpis["total_customers"] == 10000
    assert kpis["churn_rate_pct"] == 20.37
    assert kpis["active_member_pct"] == 51.51

def test_analytics_geography_endpoint(client):
    """Verifies geography churn breakdown endpoint."""
    resp = client.get("/api/v1/analytics/geography")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert len(data) == 3
    countries = {d["Geography"] for d in data}
    assert countries == {"France", "Germany", "Spain"}

def test_analytics_query_safety(client):
    """Verifies that dangerous SQL mutations are safely blocked with 400."""
    resp = client.post("/api/v1/analytics/query", json={"custom_sql": "DROP TABLE churn;"})
    assert resp.status_code == 400

def test_analytics_named_query(client):
    """Verifies that named business queries execute via query endpoint."""
    resp = client.post("/api/v1/analytics/query", json={"named_query": "churn_by_gender"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["row_count"] == 2
    assert "execution_time_ms" in data
