"""Inference service for real-time and batch customer churn prediction."""
import logging
from typing import Dict, Any, List, Optional
import joblib
import numpy as np
import pandas as pd
from src.config import settings

logger = logging.getLogger(__name__)

class ChurnPredictor:
    """Predictor class that loads the trained pipeline and scores customer profiles."""
    
    _instance = None
    _artifact = None
    
    def __init__(self, model_path: Optional[str] = None):
        path = model_path or settings.MODEL_PATH
        if ChurnPredictor._artifact is None:
            logger.info(f"Loading churn model artifact from {path}")
            ChurnPredictor._artifact = joblib.load(path)
            
        self.artifact = ChurnPredictor._artifact
        self.pipeline = self.artifact["pipeline"]
        self.model_name = self.artifact["champion_model_name"]
        self.optimal_threshold = self.artifact["optimal_threshold"]
        self.feature_names = self.artifact["feature_names"]
        
    def _extract_risk_factors(self, data: Dict[str, Any], prob: float) -> List[str]:
        """Identifies customer-specific risk drivers based on domain rules and feature importance."""
        factors = []
        
        # 1. Product count risk
        products = data.get("NumOfProducts", 1)
        if products >= 3:
            factors.append(f"Extreme product count risk: Holding {products} products historically shows over 80% churn.")
        elif products == 1:
            factors.append("Single product dependency: Customer holds only 1 product, increasing vulnerability.")
            
        # 2. Activity status
        if data.get("IsActiveMember", 0) == 0:
            factors.append("Inactive member: Customer has low recent banking engagement.")
            
        # 3. Demographic & Geographic risk
        if data.get("Geography", "").title() == "Germany":
            factors.append("Regional market vulnerability: German accounts exhibit roughly double the churn rate of France/Spain.")
            
        age = data.get("Age", 30)
        if age >= 50:
            factors.append(f"High-risk age demographic: Customer is {age} years old (attrition spikes in 45-65 age group).")
        elif age >= 40:
            factors.append(f"Moderate age risk: Customer is {age} years old.")
            
        # 4. Financial characteristics
        balance = data.get("Balance", 0.0)
        salary = data.get("EstimatedSalary", 100000.0)
        credit_score = data.get("CreditScore", 650)
        
        if balance > 100000:
            factors.append(f"High balance capital risk: Significant liquid capital (${balance:,.2f}) at risk of flight.")
        elif balance == 0:
            factors.append("Zero balance: Depleted funds indicate possible account abandonment.")
            
        if credit_score < 500:
            factors.append(f"Subprime credit score: Credit score of {credit_score} indicates credit stress.")
            
        if not factors and prob > 0.30:
            factors.append("Combined interaction of demographic and financial indicators.")
            
        return factors

    def _determine_retention_strategy(self, risk_tier: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Formulates targeted retention recommendations based on risk tier and customer profile."""
        if risk_tier == "High":
            action = "Immediate High-Touch Intervention"
            recommendations = [
                "Assign senior relationship manager for personal outreach within 48 hours.",
                "Review pricing, fee structures, or interest rate terms to match market competitors.",
                "Offer complimentary premier banking services or fee-waiver package."
            ]
        elif risk_tier == "Medium":
            action = "Targeted Value-Add Engagement"
            recommendations = [
                "Enroll in automated digital re-engagement campaign highlighting underutilized features.",
                "Offer tailored product bundling incentives (e.g. savings account interest booster).",
                "Deploy proactive customer satisfaction survey to identify pain points."
            ]
        else:
            action = "Standard Lifecycle Engagement"
            recommendations = [
                "Maintain scheduled periodic touchpoints and newsletters.",
                "Encourage mobile banking and digital feature adoption.",
                "Monitor for unexpected drops in transaction volume or account balance."
            ]
            
        return {
            "intervention_type": action,
            "actionable_steps": recommendations
        }

    def predict_single(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generates churn prediction and risk assessment for a single customer."""
        df = pd.DataFrame([customer_data])
        
        # Calculate probability
        prob = float(self.pipeline.predict_proba(df)[0, 1])
        is_churn = bool(prob >= self.optimal_threshold)
        
        # Determine risk tier
        if prob < 0.25:
            risk_tier = "Low"
        elif prob < 0.55:
            risk_tier = "Medium"
        else:
            risk_tier = "High"
            
        risk_factors = self._extract_risk_factors(customer_data, prob)
        strategy = self._determine_retention_strategy(risk_tier, customer_data)
        
        return {
            "churn_probability": round(prob, 4),
            "churn_probability_pct": round(prob * 100, 2),
            "predicted_churn": is_churn,
            "risk_tier": risk_tier,
            "decision_threshold": self.optimal_threshold,
            "model_champion": self.model_name,
            "primary_risk_factors": risk_factors,
            "retention_strategy": strategy
        }

    def predict_batch(self, df: pd.DataFrame) -> pd.DataFrame:
        """Scores a DataFrame of customer records, returning enriched predictions."""
        df_scored = df.copy()
        probs = self.pipeline.predict_proba(df)[:, 1]
        df_scored["churn_probability"] = np.round(probs, 4)
        df_scored["predicted_churn"] = (probs >= self.optimal_threshold).astype(int)
        df_scored["risk_tier"] = pd.cut(
            probs,
            bins=[-np.inf, 0.25, 0.55, np.inf],
            labels=["Low", "Medium", "High"]
        )
        return df_scored

predictor = None

def get_predictor() -> ChurnPredictor:
    """Helper to access singleton predictor instance."""
    global predictor
    if predictor is None:
        predictor = ChurnPredictor()
    return predictor
