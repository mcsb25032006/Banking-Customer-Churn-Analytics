"""Pydantic v2 data models for API request and response validation."""
from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class CustomerInput(BaseModel):
    """Input features required for customer churn prediction."""
    model_config = ConfigDict(extra="forbid")
    
    CreditScore: int = Field(..., ge=300, le=850, description="Credit score between 300 and 850", json_schema_extra={"example": 650})
    Geography: Literal["France", "Germany", "Spain"] = Field(..., description="Customer banking market country", json_schema_extra={"example": "Germany"})
    Gender: Literal["Female", "Male"] = Field(..., description="Customer gender", json_schema_extra={"example": "Female"})
    Age: int = Field(..., ge=18, le=100, description="Customer age in years", json_schema_extra={"example": 45})
    Tenure: int = Field(..., ge=0, le=10, description="Years customer has maintained accounts", json_schema_extra={"example": 5})
    Balance: float = Field(..., ge=0.0, description="Current account balance in USD", json_schema_extra={"example": 75000.0})
    NumOfProducts: int = Field(..., ge=1, le=4, description="Number of bank products held (1-4)", json_schema_extra={"example": 1})
    HasCrCard: int = Field(..., ge=0, le=1, description="Whether customer holds a credit card (1=Yes, 0=No)", json_schema_extra={"example": 1})
    IsActiveMember: int = Field(..., ge=0, le=1, description="Active customer status indicator (1=Active, 0=Inactive)", json_schema_extra={"example": 0})
    EstimatedSalary: float = Field(..., ge=0.0, description="Estimated customer annual salary in USD", json_schema_extra={"example": 105000.0})

class RetentionStrategy(BaseModel):
    intervention_type: str
    actionable_steps: List[str]

class PredictionResponse(BaseModel):
    """Response schema for single customer churn prediction."""
    churn_probability: float = Field(..., description="Predicted churn probability between 0 and 1")
    churn_probability_pct: float = Field(..., description="Churn probability percentage")
    predicted_churn: bool = Field(..., description="Binary classification at optimal decision threshold")
    risk_tier: Literal["Low", "Medium", "High"] = Field(..., description="Categorical risk classification")
    decision_threshold: float = Field(..., description="Applied decision threshold")
    model_champion: str = Field(..., description="Algorithm used for inference")
    primary_risk_factors: List[str] = Field(..., description="Key features driving the prediction")
    retention_strategy: RetentionStrategy = Field(..., description="Prescriptive retention action plan")

class BatchPredictionRequest(BaseModel):
    customers: List[CustomerInput] = Field(..., min_length=1, max_length=1000)

class BatchPredictionResponse(BaseModel):
    total_scored: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    predictions: List[PredictionResponse]

class QueryRequest(BaseModel):
    named_query: Optional[str] = Field(None, description="Key of a pre-configured business query")
    custom_sql: Optional[str] = Field(None, description="Custom read-only SQL query against the 'churn' table")

class QueryResponse(BaseModel):
    columns: List[str]
    rows: List[Dict[str, Any]]
    row_count: int
    execution_time_ms: float

class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    model_loaded: bool
    database_connected: bool
