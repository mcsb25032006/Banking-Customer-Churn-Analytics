"""Business Analytics and SQL Query endpoints."""
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, status
from src.db.sql_runner import run_business_query, execute_query, CORE_BUSINESS_QUERIES
from src.api.schemas import QueryRequest, QueryResponse

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics & SQL"])

@router.get("/kpis")
def get_executive_kpis():
    """Retrieves high-level executive churn KPIs."""
    try:
        res = run_business_query("executive_kpis")
        return {
            "kpis": res["rows"][0] if res["rows"] else {},
            "benchmark_ms": res["execution_time_ms"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/geography")
def get_geography_churn():
    """Retrieves churn distribution across geographic markets."""
    try:
        res = run_business_query("churn_by_geography")
        return {"data": res["rows"], "benchmark_ms": res["execution_time_ms"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/demographics")
def get_demographics_churn():
    """Retrieves churn breakdown across age groups and gender."""
    try:
        age_res = run_business_query("churn_by_age_group")
        gender_res = run_business_query("churn_by_gender")
        return {
            "by_age_group": age_res["rows"],
            "by_gender": gender_res["rows"],
            "benchmark_ms": round(age_res["execution_time_ms"] + gender_res["execution_time_ms"], 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products")
def get_product_churn():
    """Retrieves churn rate stratified by number of banking products."""
    try:
        res = run_business_query("churn_by_products")
        return {"data": res["rows"], "benchmark_ms": res["execution_time_ms"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/risk-segments")
def get_high_risk_segments():
    """Retrieves top 10 highest-churn multi-dimensional customer segments using SQL CTEs and window ranking."""
    try:
        res = run_business_query("high_risk_segments")
        return {"segments": res["rows"], "benchmark_ms": res["execution_time_ms"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/available-queries")
def list_available_queries():
    """Lists pre-configured business queries."""
    return {"queries": list(CORE_BUSINESS_QUERIES.keys())}

@router.post("/query", response_model=QueryResponse)
def execute_sql(payload: QueryRequest):
    """Executes a pre-defined named business query or safe read-only custom SQL query."""
    try:
        if payload.named_query:
            res = run_business_query(payload.named_query)
        elif payload.custom_sql:
            res = execute_query(payload.custom_sql)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Must provide either 'named_query' or 'custom_sql'."
            )
        return QueryResponse(**res)
    except ValueError as val_err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(val_err))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
