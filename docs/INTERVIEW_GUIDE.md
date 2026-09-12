# Banking Customer Churn Analytics: Technical Interview & Defense Guide

This guide prepares you to discuss the architecture, engineering choices, machine learning models, database design, and production patterns of this project in technical interviews.

---

## 1. Project Pitch & Executive Summary

### 30-Second Elevator Pitch
> *"I designed and built an end-to-end Banking Customer Churn Analytics and Machine Learning platform. The system ingests and models 10,000 retail banking accounts, using advanced SQL window functions and CTEs for cohort analysis alongside an automated Machine Learning pipeline (XGBoost champion, 0.867 ROC-AUC). I packaged the solution into a production FastAPI microservice with strict Pydantic v2 data validation, automated risk factor explainability, prescriptive retention recommendations, and an interactive web dashboard for real-time risk scoring."*

---

## 2. System Architecture & Component Walkthrough

```
                                [ CLIENT / BROWSER ]
                                         |
                       HTTP / REST (JSON) | Interactive SPA
                                         v
+-----------------------------------------------------------------------------------+
|                           FASTAPI APPLICATION LAYER                               |
|                                                                                   |
|   /health               /api/v1/predict           /api/v1/analytics              |
|   (Telemetry)           (Real-Time & Batch)       (KPIs, SQL Runner)             |
|          |                      |                         |                       |
|          |                      v                         v                       |
|          |             [ Pydantic v2 Schemas ]   [ SQL Query Runner ]             |
+----------|----------------------|-------------------------|-----------------------+
           |                      |                         |
           v                      v                         v
   [ System Check ]     [ ML Pipeline Engine ]     [ SQLite / Postgres DB ]
                        - Feature Engineering       - 'churn' table (indexed)
                        - StandardScaler / OHE      - 67 Business Queries
                        - XGBoost Classifier        - Window ranking & CTEs
                        - Risk Driver Explainers
```

### Key Engineering Decisions:
1. **Why FastAPI instead of Flask or Django?**
   * **Native Async & Performance**: ASGI architecture handles concurrent requests with low latency.
   * **Pydantic v2 Integration**: Type hints give automated data serialization, input validation, and automatic OpenAPI / Swagger documentation out-of-the-box.
   * **Lightweight Footprint**: Avoids the heavy ORM/admin overhead of Django while providing greater structure and validation than raw Flask.

2. **Why SQLite by default with SQLAlchemy abstraction?**
   * **Zero-friction Portability**: The original project required a local Microsoft SQL Server instance with Windows-specific ODBC drivers. Abstracting via SQLAlchemy 2.0 with an SQLite file database allows the entire system to run cross-platform (macOS, Linux, Docker, Windows) without external infrastructure.
   * **Production-Ready Switch**: Switching to PostgreSQL only requires updating the `DATABASE_URL` environment variable.

---

## 3. Machine Learning Deep Dive

### 1. Data Characteristics & Class Imbalance
* **Total Records**: 10,000 customers.
* **Target Distribution**: 7,963 retained (79.63%), 2,037 churned (20.37%).
* **Imbalance Ratio**: Approximately 4:1.
* **How class imbalance was addressed**:
  * Used `StratifiedKFold` (5 splits) and stratified train/test split to guarantee identical churn proportions in every fold.
  * Configured `scale_pos_weight = 3.9` (and `class_weight="balanced"`) so the loss function penalizes false negatives proportionally.
  * Evaluated on **ROC-AUC** and **PR-AUC (Average Precision)** rather than raw Accuracy (which would misleadingly show ~80% even for a trivial dummy classifier).

### 2. Candidate Algorithm Comparison
| Model | CV ROC-AUC | Test ROC-AUC | Test PR-AUC | Tuned Recall | Tuned Precision | Tuned F1 | Brier Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** (Baseline) | 0.7678 | 0.7786 | 0.4966 | 61.4% | 44.4% | 0.5155 | 0.1945 |
| **Random Forest** | 0.8546 | 0.8564 | 0.6932 | 62.7% | 63.1% | 0.6289 | 0.1335 |
| **LightGBM** | 0.8550 | 0.8589 | 0.7044 | 72.5% | 52.9% | 0.6295 | 0.1316 |
| **XGBoost (Champion)** | **0.8565** | **0.8668** | **0.7158** | **66.8%** | **60.6%** | **0.6355** | **0.1348** |

### 3. Feature Engineering
We engineered 5 domain-specific features using a custom scikit-learn transformer (`BankingFeatureEngineer`):
1. **`BalanceSalaryRatio`** (`Balance / EstimatedSalary`): Identifies high-net-worth customers whose account balance is disengaged from annual earnings.
2. **`TenureAgeRatio`** (`Tenure / Age`): Quantifies the percentage of the customer's adult life spent banking with this institution.
3. **`CreditScoreAgeRatio`** (`CreditScore / Age`): Financial health index relative to lifecycle stage.
4. **`ProductsPerTenure`** (`NumOfProducts / Tenure`): Velocity of product adoption.
5. **`IsZeroBalance`** (`Balance == 0`): Captures binary behavior of fully depleted or dormant accounts.

### 4. Optimal Decision Threshold Tuning
* **Concept**: Default binary classification uses a 0.50 threshold. In banking churn, **False Negatives** (failing to detect a churner who walks away with assets) are significantly more expensive than **False Positives** (sending a retention coupon to a customer who wasn't leaving).
* **Implementation**: We calculated the Precision-Recall curve across candidate thresholds [0.20 to 0.60] to optimize the F1-score and calibrated operational recall to over 66% while maintaining precision > 60%.

### 5. Top Feature Importances (What drives churn?)
1. **`NumOfProducts` (19.4%)**: Customers with 1 product are vulnerable; customers with 3 or 4 products churn at an alarming rate (>80%), signaling fee fatigue, product dissatisfaction, or cross-sell misaligned with customer needs.
2. **`Age` (15.8%)**: Churn rate surges in the 45-65 age group (wealth accumulation & retirement consolidation stage).
3. **`IsActiveMember` (13.8%)**: Lack of digital / account activity is a primary early-warning indicator.
4. **`IsZeroBalance` (12.6%)**: Accounts with zero balance have high exit velocity.
5. **`Geography_Germany` (8.1%)**: German customers exhibit over double the churn rate (32.4%) compared to France (16.1%) and Spain (16.7%).

---

## 4. SQL Analytics & Database Engineering

### 1. Complex Query Example: CTE with Window Function `RANK()`
```sql
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
```
* **Why use a CTE?** Encapsulates multi-level aggregation and filtering (`HAVING COUNT(*) >= 20`), ensuring statistical significance before calculating rank.
* **Why use `RANK() OVER (...)`?** Assigns deterministic ranking based on churn rate while correctly handling ties.

---

## 5. Frequently Asked Interview Questions & Answers

### Q1: How did you prevent data leakage during feature engineering and model training?
**Answer**:
> *"All preprocessing transformations (imputation, scaling, one-hot encoding, and feature interactions) were wrapped inside a unified Scikit-Learn `Pipeline` and `ColumnTransformer`. The train/test split was performed strictly before any fitting. The scaler and encoder were fitted only on the training folds and applied to test folds during cross-validation, guaranteeing zero statistical information from test sets leaked into training."*

### Q2: Why did XGBoost outperform Logistic Regression by nearly 9% ROC-AUC?
**Answer**:
> *"Logistic Regression assumes linear relationships and additive effects on log-odds. Banking churn in this dataset is highly non-linear and governed by complex feature interactions—for example, holding multiple products is safe for young active members in France, but exhibits over 80% churn when combined with older inactive accounts in Germany. Gradient-boosted decision trees naturally partition feature space to capture these non-linear thresholds and multi-way interactions."*

### Q3: How do you explain the predictions to non-technical banking stakeholders?
**Answer**:
> *"Rather than returning a raw black-box probability, the API maps probabilities into three actionable risk tiers: Low (<25%), Medium (25-55%), and High (>=55%). Crucially, the response provides rule-based explainability identifying the customer's specific drivers (e.g. 'German account', 'Single product', 'Age 52') paired with prescriptive retention actions (e.g. 'Assign dedicated relationship manager within 48 hours')."*

### Q4: How would you monitor this model in production?
**Answer**:
> *"I would monitor three pillars:*
> 1. *Data Drift*: Monitor distribution drift of incoming numerical features (using Kolmogorov-Smirnov test) and categorical features (using PSI / Population Stability Index).
> 2. *Concept Drift*: Periodically evaluate prediction accuracy against actual churn outcomes as customers close accounts 30-90 days later.
> 3. *Operational Health*: Track latency (p95/p99 under 50ms), HTTP error rates, and batch prediction throughput.*"

### Q5: What were the original project files, and what did you build?
**Answer**:
> *"The original repository was a data analytics study consisting of an exploratory Jupyter notebook, T-SQL queries for MS SQL Server, and a Power BI file. I transformed it into a production software system by:*
> * *Building an automated database ETL and query runner compatible with standard SQL and SQLite/Postgres.*
> * *Designing, training, and benchmarking an end-to-end Machine Learning pipeline with custom feature engineering and threshold optimization.*
> * *Developing a high-performance FastAPI microservice with strict Pydantic v2 validation.*
> * *Building an interactive web dashboard with live prediction simulator and analytics charts.*
> * *Authoring 21 automated unit, ML, and API integration tests with 100% pass rate.*
> * *Containerizing the application with Docker and Docker Compose."*
