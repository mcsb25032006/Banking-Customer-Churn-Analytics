# 🏦 Banking Customer Churn Analytics

> **End-to-end Banking Customer Churn Analytics using Python, SQL Server & Power BI**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![SQL Server](https://img.shields.io/badge/SQL%20Server-T--SQL-CC2927?style=for-the-badge\&logo=microsoftsqlserver\&logoColor=white)](https://www.microsoft.com/sql-server)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=for-the-badge\&logo=powerbi\&logoColor=black)](https://powerbi.microsoft.com/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge\&logo=pandas\&logoColor=white)](https://pandas.pydata.org/)

---

## 📊 Project at a Glance

| Metric                  |                              Value |
| ----------------------- | ---------------------------------: |
| 👥 Total Customers      |                         **10,000** |
| 📉 Churned Customers    |                          **2,037** |
| 📊 Overall Churn Rate   |                         **20.37%** |
| 🧮 SQL Business Queries |                             **67** |
| 📈 Power BI Dashboards  |                              **7** |
| 🛠️ Core Technologies   | **Python · SQL Server · Power BI** |

---

## 📝 Project Overview

This project presents a comprehensive **end-to-end banking customer churn analytics solution** built using **Python, SQL Server, and Power BI**.

The primary objective is to transform raw banking customer data into **actionable business insights** that support:

* Customer retention
* Churn identification
* Customer segmentation
* Risk assessment
* Product engagement analysis
* Strategic decision-making

The project covers the complete analytics lifecycle:

```text
Raw Customer Data
       │
       ▼
┌─────────────────┐
│ Python          │
│ ETL + EDA       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ SQL Server      │
│ Business        │
│ Analysis        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Power BI        │
│ KPIs +          │
│ Dashboards      │
└────────┬────────┘
         │
         ▼
 Actionable Business
      Insights
```

The final solution contains **67 SQL business queries** and **7 interactive Power BI dashboards**, providing a multidimensional view of customer churn, demographics, engagement, banking-product usage, financial characteristics, geography, and customer risk.

---

# 🎯 Business Problem

Banking institutions generate large volumes of customer data through:

* Account activity
* Banking-product usage
* Customer demographics
* Financial characteristics
* Geographic information
* Customer interactions

Without structured analysis, valuable opportunities to **identify at-risk customers and improve retention** can easily be overlooked.

### The business challenge

> **How can banking customer data be transformed into actionable insights that help identify churn patterns, understand customer behaviour, and support effective retention strategies?**

This project addresses that challenge by integrating:

| Technology         | Purpose                                                |
| ------------------ | ------------------------------------------------------ |
| 🐍 **Python**      | Data cleaning, preparation & Exploratory Data Analysis |
| 🗄️ **SQL Server** | Business analysis, segmentation & advanced SQL         |
| 📊 **Power BI**    | KPI reporting, visualization & interactive dashboards  |

---

# 🚀 Project Objectives

The project focuses on the following objectives:

* 🧹 Clean and prepare banking customer data
* 🔍 Perform data preparation and Exploratory Data Analysis using Python
* 🧮 Develop advanced SQL analytical queries
* 📉 Analyse overall customer churn and retention
* 📊 Create executive churn KPIs
* 👥 Analyse customer demographics
* 📱 Analyse customer activity and engagement
* 🏦 Evaluate banking-product usage
* 💳 Analyse credit and financial characteristics
* 🌍 Analyse geographic churn patterns
* 🎯 Identify high-churn customer segments
* ⚠️ Develop customer-risk segmentation
* 📈 Build interactive Power BI dashboards
* 💡 Generate actionable customer retention recommendations

---

# 🛠️ Technologies & Tools

### Programming & Data Analysis

* Python
* Pandas
* NumPy
* Matplotlib
* Jupyter Notebook

### Database & Analytics

* Microsoft SQL Server
* T-SQL
* CTEs
* Subqueries
* Window Functions
* Ranking Functions
* Aggregations

### Business Intelligence

* Power BI
* Power Query
* DAX

---

# 🔄 ETL & Exploratory Data Analysis

The Python workflow was used to prepare the raw dataset before performing SQL-based business analysis.

### Data Preparation Pipeline

```text
Import Dataset
      ↓
Inspect Structure & Data Types
      ↓
Check Missing / Inconsistent Values
      ↓
Data Cleaning
      ↓
Feature Engineering
      ↓
Exploratory Data Analysis
      ↓
Customer Segmentation
      ↓
Export Clean Dataset
      ↓
Load into SQL Server
```

### Key ETL & EDA Activities

* Imported the banking customer churn dataset
* Inspected dataset structure and data types
* Checked for missing and inconsistent values
* Performed data cleaning and preparation
* Analysed customer demographics
* Analysed financial characteristics
* Explored customer activity and product usage
* Created analytical customer segments
* Performed Exploratory Data Analysis using Python
* Prepared the cleaned dataset for SQL Server
* Loaded the prepared dataset into SQL Server

### 🧩 Engineered Analytical Fields

Additional fields were created to support segmentation and analysis:

| Field             | Purpose                                       |
| ----------------- | --------------------------------------------- |
| `AgeGroup`        | Categorise customers into age segments        |
| `CreditScoreBand` | Group customers based on credit score         |
| `BalanceBand`     | Categorise customers based on account balance |
| `Customer_churn`  | Identify customer churn status                |

---

# 🗄️ SQL Business Analysis

A total of **67 SQL business queries** were developed to analyse customer churn from multiple business perspectives.

### Analysis Areas

| Analysis Category              | Focus                                  |
| ------------------------------ | -------------------------------------- |
| 📊 Executive Churn Overview    | Overall churn & retention KPIs         |
| 👥 Customer Demographics       | Age, gender & customer characteristics |
| ⏳ Age & Tenure Analysis        | Customer lifecycle & tenure patterns   |
| 🏦 Product & Engagement        | Banking products & customer activity   |
| 💳 Financial & Credit Analysis | Credit scores, balances & salaries     |
| 🌍 Geography & Behaviour       | Geographic and behavioural patterns    |
| ⚠️ Customer Risk Analysis      | High-risk customer identification      |
| 🎯 Customer Segmentation       | Advanced churn segmentation            |

### Advanced SQL Techniques

The project demonstrates practical use of:

* `SELECT`
* `WHERE`
* `GROUP BY`
* `HAVING`
* Aggregations
* Filtering
* Subqueries
* Common Table Expressions (**CTEs**)
* Window Functions
* `RANK()`
* Churn-rate calculations
* Customer segmentation
* Multi-dimensional analysis
* Customer risk scoring

---

# 📊 Power BI Dashboards

The final Power BI solution contains **7 interactive dashboards**, each designed around a specific business question.

---

## 1. 📌 Executive Churn Overview

Provides an executive-level view of customer retention performance.

### Key focus areas

* Total customers
* Churned customers
* Churn rate
* Customer activity
* Overall retention performance

**Business purpose:**
Provide decision-makers with a quick overview of the organization's customer churn position.

---

## 2. 👥 Customer Demographics & Churn

Explores how customer demographics influence churn.

### Analysis includes

* Geography
* Gender
* Age groups
* Demographic churn patterns

**Business purpose:**
Identify demographic segments with elevated churn rates.

---

## 3. 🏦 Customer Engagement & Banking Products

Evaluates the relationship between customer engagement, activity, and banking-product usage.

### Analysis includes

* Active vs. inactive customers
* Number of banking products
* Credit-card ownership
* Customer engagement
* Product usage
* Churn behaviour

**Business purpose:**
Understand whether engagement and product adoption are associated with customer retention.

---

## 4. 💳 Financial & Credit Analysis

Analyses customer financial characteristics and their relationship with churn.

### Analysis includes

* Credit scores
* Account balances
* Estimated salaries
* Credit-score bands
* Balance bands
* Churn behaviour

**Business purpose:**
Understand financial characteristics associated with different churn patterns.

---

## 5. 🌍 Geography & Customer Behaviour

Analyses customer behaviour across geographic markets.

### Analysis includes

* Geographic churn
* Gender
* Activity status
* Banking-product usage
* Geographic customer segments

**Business purpose:**
Identify geographic markets and behavioural combinations associated with higher churn.

---

## 6. ⚠️ Customer Risk Analysis

Identifies customer segments that demonstrate elevated churn risk.

### Analysis includes

* Customer activity
* Age
* Product usage
* Geography
* Customer characteristics
* Churn risk patterns

**Business purpose:**
Help identify customers who may require proactive retention interventions.

---

## 7. 🎯 Advanced Customer Risk & Retention

Provides deeper customer-risk segmentation and identifies high-churn customer groups.

### Focus areas

* Advanced segmentation
* High-churn customer groups
* Risk characteristics
* Retention opportunities
* Targeted customer strategies

**Business purpose:**
Translate analytical findings into actionable customer retention strategies.

---

# 💡 Key Business Insights

The analysis generated several important findings:

### 📉 Churn

* The dataset contains **10,000 customers**.
* **2,037 customers have churned**.
* The overall customer churn rate is **20.37%**.

### 🌍 Geography

* Customer churn varies significantly across geographic markets.
* **Germany records the highest churn rate** among the three geographies.

### 📱 Customer Engagement

* Inactive customers demonstrate considerably higher churn than active customers.
* Customer engagement is an important dimension when evaluating churn risk.

### 🏦 Product Usage

* Churn varies across customers with different numbers of banking products.
* Banking-product adoption provides an additional dimension for customer segmentation.

### 👥 Demographics

* Customer age shows differences in churn behaviour across age groups.
* Demographic characteristics can help identify high-risk customer segments.

### 💳 Financial Characteristics

* Credit score, account balance, and estimated salary provide additional dimensions for understanding churn behaviour.

### 🎯 Multi-dimensional Risk

* Certain combinations of **geography, age, activity status, and product usage** demonstrate higher churn rates.
* Combining multiple customer characteristics provides stronger segmentation opportunities than analysing individual variables in isolation.

---

# 💼 Business Recommendations

Based on the analysis, the following strategies are recommended:

### 1. Re-engage Inactive Customers

Prioritize inactive customers through:

* Proactive communication
* Personalized offers
* Account reactivation campaigns
* Engagement-focused services

### 2. Investigate German Market Churn

Germany demonstrates the highest churn rate among the analysed geographies.

Further investigation should focus on:

* Customer experience
* Product-market fit
* Pricing
* Competitor activity
* Service quality
* Customer support

### 3. Target High-Churn Demographic Segments

Develop personalized retention strategies for demographic groups exhibiting elevated churn.

### 4. Monitor Customer Activity

Customer inactivity can serve as a potential **early warning indicator** of customer attrition.

### 5. Review Product Adoption

Analyse banking-product usage among high-churn segments and identify opportunities for:

* Cross-selling
* Product bundling
* Product education
* Customer engagement

### 6. Personalize Customer Engagement

Use customer demographics, activity, product usage, and financial characteristics to develop targeted engagement strategies.

### 7. Establish Continuous Risk Monitoring

Continuously identify and monitor high-risk customer segments using Power BI and SQL analytics.

### 8. Monitor Churn KPIs

Use the Power BI dashboards to regularly track:

* Churn rate
* Churn volume
* Customer activity
* Geographic churn
* Segment-level churn

### 9. Future Enhancement — Predictive Churn Modelling

A future phase could introduce **machine-learning-based predictive churn modelling** to estimate the probability of individual customers leaving before churn occurs.

Potential models could include:

* Logistic Regression
* Decision Trees
* Random Forest
* XGBoost
* Gradient Boosting

---

# 📁 Repository Structure

```text
Banking_Customer_Churn_Analytics/
│
├── 📂 Dashboard_Screenshots/
│
├── 📂 Documentation/
│   ├── 📄 Business Problem Statement
│   └── 📄 Project Report
│
├── 📂 Python/
│   └── 📓 Banking_Customer_Churn_EDA.ipynb
│
├── 📂 SQL/
│   └── 📄 Banking_Customer_Churn.sql
│
├── 📂 PowerBI/
│   └── 📊 Banking_Customer_Churn_Analytics.pbix
│
└── 📄 README.md
```

---

# 🧠 Skills Demonstrated

This project demonstrates practical experience across the complete **Data Analytics → Business Intelligence** workflow.

### Data Analytics

* Data Cleaning
* Exploratory Data Analysis
* Feature Engineering
* Customer Segmentation
* Business Analysis

### SQL

* Advanced T-SQL
* CTEs
* Subqueries
* Window Functions
* Ranking
* Aggregations
* Churn-rate calculations

### Power BI

* Dashboard Development
* KPI Design
* Interactive Visualizations
* Customer Segmentation
* Business Reporting
* Data Storytelling

### Business Intelligence

* Churn Analysis
* Customer Retention
* Risk Identification
* Geographic Analysis
* Customer Behaviour Analysis
* Actionable Recommendations

---

# 🔮 Future Scope

The project can be further enhanced by introducing:

* 🤖 Predictive customer churn modelling
* 📈 Individual customer churn probability
* ⚠️ Automated customer risk scoring
* 🔔 Early-warning churn alerts
* 🎯 Next-best-action recommendations
* 📊 Customer lifetime value analysis
* 🔄 Automated data refresh pipelines
* ☁️ Cloud-based deployment
* 🧠 Machine-learning-driven customer segmentation

---

# 🏁 Conclusion

This project demonstrates how **Python, SQL Server, and Power BI** can be integrated into a complete end-to-end analytics solution.

Starting from raw customer data, the project progresses through:

> **Data Cleaning → EDA → SQL Analysis → Customer Segmentation → KPI Development → Power BI Dashboards → Business Recommendations**

With **67 SQL business queries** and **7 interactive dashboards**, the solution provides a comprehensive framework for understanding customer churn, identifying high-risk segments, and supporting data-driven customer retention strategies.

---

## ⭐ Project Highlights

```text
🐍 Python
   ↓
🧹 Data Cleaning & EDA
   ↓
🗄️ SQL Server
   ↓
🧮 67 Business Queries
   ↓
📊 Power BI
   ↓
📈 7 Interactive Dashboards
   ↓
💡 Customer Churn Insights
   ↓
🎯 Retention Strategies
```

> **Built to turn customer data into actionable retention intelligence.**
