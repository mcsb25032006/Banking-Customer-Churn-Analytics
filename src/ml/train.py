"""Machine learning training and model evaluation pipeline.

Trains multiple classification algorithms (Logistic Regression, Random Forest,
LightGBM, XGBoost) on stratified splits, evaluates discrimination (ROC-AUC, PR-AUC)
and calibration, determines the optimal decision threshold, and exports serialized artifacts.
"""
import json
import logging
from datetime import datetime
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
import lightgbm as lgb
import xgboost as xgb

from src.config import settings
from src.ml.features import (
    BankingFeatureEngineer,
    RAW_NUMERIC_FEATURES,
    CATEGORICAL_FEATURES,
    TARGET_COLUMN,
    create_preprocessor
)

logging.basicConfig(level=settings.LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def load_data():
    """Loads raw dataset and prepares feature matrix X and target y."""
    df = pd.read_csv(settings.RAW_DATA_PATH)
    logger.info(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    
    feature_cols = RAW_NUMERIC_FEATURES + CATEGORICAL_FEATURES
    X = df[feature_cols]
    y = df[TARGET_COLUMN]
    return X, y

def evaluate_predictions(y_true, y_prob, threshold=0.5):
    """Calculates comprehensive classification metrics."""
    y_pred = (y_prob >= threshold).astype(int)
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    return {
        "threshold": round(float(threshold), 3),
        "roc_auc": round(float(roc_auc_score(y_true, y_prob)), 4),
        "pr_auc": round(float(average_precision_score(y_true, y_prob)), 4),
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
        "brier_score": round(float(brier_score_loss(y_true, y_prob)), 4),
        "confusion_matrix": {
            "true_negatives": int(tn),
            "false_positives": int(fp),
            "false_negatives": int(fn),
            "true_positives": int(tp)
        }
    }

def find_optimal_threshold(y_true, y_prob):
    """Finds classification threshold that maximizes F1 score."""
    precisions, recalls, thresholds = precision_recall_curve(y_true, y_prob)
    f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)
    best_idx = np.argmax(f1_scores)
    # thresholds array is 1 element shorter than precisions/recalls
    best_thresh = thresholds[min(best_idx, len(thresholds) - 1)]
    return float(np.clip(best_thresh, 0.20, 0.60))

def train_and_evaluate():
    """Executes model training, comparative benchmark, and artifact persistence."""
    X, y = load_data()
    
    # 80/20 Stratified train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    logger.info(f"Training set: {len(X_train)} samples, Test set: {len(X_test)} samples")
    
    # Candidate models
    candidate_models = {
        "Logistic_Regression": LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42),
        "Random_Forest": RandomForestClassifier(n_estimators=200, max_depth=10, class_weight="balanced", random_state=42, n_jobs=-1),
        "LightGBM": lgb.LGBMClassifier(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=6,
            num_leaves=31,
            scale_pos_weight=3.9,  # ~ (1-0.2037)/0.2037
            random_state=42,
            verbosity=-1
        ),
        "XGBoost": xgb.XGBClassifier(
            n_estimators=150,
            learning_rate=0.05,
            max_depth=5,
            scale_pos_weight=3.9,
            random_state=42,
            eval_metric="logloss"
        )
    }
    
    benchmark_results = {}
    best_model_name = None
    best_pipeline = None
    best_roc_auc = -1.0
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    for name, clf in candidate_models.items():
        logger.info(f"Evaluating {name}...")
        pipeline = Pipeline([
            ("engineer", BankingFeatureEngineer()),
            ("preprocessor", create_preprocessor()),
            ("classifier", clf)
        ])
        
        # 5-fold cross-validation on train set
        cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="roc_auc", n_jobs=-1)
        mean_cv = float(np.mean(cv_scores))
        std_cv = float(np.std(cv_scores))
        
        # Fit on full training set
        pipeline.fit(X_train, y_train)
        
        # Predict probabilities on test set
        y_test_prob = pipeline.predict_proba(X_test)[:, 1]
        default_metrics = evaluate_predictions(y_test, y_test_prob, threshold=0.5)
        
        optimal_thresh = find_optimal_threshold(y_test, y_test_prob)
        tuned_metrics = evaluate_predictions(y_test, y_test_prob, threshold=optimal_thresh)
        
        benchmark_results[name] = {
            "cv_roc_auc_mean": round(mean_cv, 4),
            "cv_roc_auc_std": round(std_cv, 4),
            "test_default_threshold": default_metrics,
            "test_optimal_threshold": tuned_metrics
        }
        logger.info(f"{name} -> CV ROC-AUC: {mean_cv:.4f} (+/- {std_cv:.4f}), Test ROC-AUC: {default_metrics['roc_auc']}, Tuned F1: {tuned_metrics['f1']} @ thresh {optimal_thresh:.2f}")
        
        if default_metrics["roc_auc"] > best_roc_auc:
            best_roc_auc = default_metrics["roc_auc"]
            best_model_name = name
            best_pipeline = pipeline
            
    logger.info(f"Champion Model selected: {best_model_name} with Test ROC-AUC: {best_roc_auc:.4f}")
    
    # Finalize champion model
    champion_optimal_thresh = benchmark_results[best_model_name]["test_optimal_threshold"]["threshold"]
    
    # Extract feature names & importances
    preprocessor = best_pipeline.named_steps["preprocessor"]
    cat_names = list(preprocessor.named_transformers_["cat"].get_feature_names_out(CATEGORICAL_FEATURES))
    num_names = preprocessor.named_transformers_["num"].feature_names_in_.tolist()
    all_feature_names = num_names + cat_names
    
    classifier = best_pipeline.named_steps["classifier"]
    feature_importances = {}
    if hasattr(classifier, "feature_importances_"):
        raw_importances = classifier.feature_importances_
        norm_importances = raw_importances / np.sum(raw_importances)
        feature_importances = {
            name: round(float(imp), 4)
            for name, imp in sorted(zip(all_feature_names, norm_importances), key=lambda x: x[1], reverse=True)
        }
    elif hasattr(classifier, "coef_"):
        feature_importances = {
            name: round(float(coef), 4)
            for name, coef in zip(all_feature_names, classifier.coef_[0])
        }
        
    # Serialize model artifact bundle
    model_artifact = {
        "pipeline": best_pipeline,
        "champion_model_name": best_model_name,
        "optimal_threshold": champion_optimal_thresh,
        "feature_names": all_feature_names,
        "input_numeric_features": RAW_NUMERIC_FEATURES,
        "input_categorical_features": CATEGORICAL_FEATURES,
        "feature_importances": feature_importances,
        "trained_at": datetime.utcnow().isoformat(),
        "training_samples": len(X_train),
        "test_samples": len(X_test),
        "version": "1.0.0"
    }
    
    joblib.dump(model_artifact, settings.MODEL_PATH)
    logger.info(f"Saved serialized champion model artifact to {settings.MODEL_PATH}")
    
    # Export metrics JSON
    metrics_export = {
        "champion_model": best_model_name,
        "optimal_threshold": champion_optimal_thresh,
        "trained_at": datetime.utcnow().isoformat(),
        "benchmark_comparison": benchmark_results,
        "feature_importances": feature_importances
    }
    
    with open(settings.METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics_export, f, indent=2)
    logger.info(f"Saved evaluation metrics to {settings.METRICS_PATH}")
    
    return metrics_export

if __name__ == "__main__":
    train_and_evaluate()
