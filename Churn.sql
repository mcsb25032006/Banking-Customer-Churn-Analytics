

-- COMPREHENSIVE CUSTOMER CHURN ANALYTICS
-- 67 SQL BUSINESS QUESTIONS
--===================================================================
-- KEY LOGIC USED IN THIS PROJECT
--
-- SUM(Exited) = Number of churned customers
-- COUNT(*) = Total customers
-- COUNT(*) - SUM(Exited) = Retained customers
--
-- Churn Rate:
-- SUM(Exited) / COUNT(*) * 100
--
-- We use DECIMAL and 100.0 to avoid integer division.
-- ================================================================


-- ================================================================
-- A. EXECUTIVE CHURN OVERVIEW — QUESTIONS 1–10
-- ================================================================

-- 1. What is the total number of customers?

SELECT
    COUNT(*) AS Total_Customers
FROM churn;


-- 2. How many customers have churned?

SELECT
    SUM(Exited) AS Churned_Customers
FROM churn;


-- 3. How many customers have been retained?

SELECT
    COUNT(*) - SUM(Exited) AS Retained_Customers
FROM churn;


-- 4. What is the overall customer churn rate?

SELECT
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*)
        AS Churn_Rate_Percentage
FROM churn;


-- 5. What is the overall customer retention rate?

SELECT
    CAST(COUNT(*) - SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Retention_Rate_Percentage
FROM churn;


-- 6. What is the total number of active members?

SELECT
    SUM(IsActiveMember) AS Active_Members
FROM churn;


-- 7. What percentage of customers are active members?

SELECT
    CAST(SUM(IsActiveMember) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Active_Member_Percentage
FROM churn;


-- 8. What is the average customer age?

SELECT
    ROUND(AVG(Age), 2) AS Average_Customer_Age
FROM churn;


-- 9. What is the average customer balance?

SELECT
    ROUND(AVG(Balance), 2) AS Average_Customer_Balance
FROM churn;


-- 10. What is the average customer credit score?

SELECT
    ROUND(AVG(CreditScore), 2) AS Average_Credit_Score
FROM churn;



-- ================================================================
-- B. CUSTOMER DEMOGRAPHICS — QUESTIONS 11–20
-- ================================================================

-- 11. How many customers are there in each geography?

SELECT
    Geography,
    COUNT(*) AS Total_Customers
FROM churn
GROUP BY Geography
ORDER BY Total_Customers DESC;


-- 12. What percentage of the total customer base
--     comes from each geography?

SELECT
    Geography,
    COUNT(*) AS Total_Customers,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS Customer_Percentage
FROM churn
GROUP BY Geography
ORDER BY Customer_Percentage DESC;


-- 13. How many customers are there by gender?

SELECT
    Gender,
    COUNT(*) AS Total_Customers
FROM churn
GROUP BY Gender
ORDER BY Total_Customers DESC;


-- 14. What percentage of customers belong to each gender?

SELECT
    Gender,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS Customer_Percentage
FROM churn
GROUP BY Gender
ORDER BY Customer_Percentage DESC;


-- 15. What is the churn rate by geography?

SELECT
    Geography,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY Geography
ORDER BY Churn_Rate_Percentage DESC;


-- 16. Which geography has the highest churn rate?

SELECT TOP 1
    Geography,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY Geography
ORDER BY Churn_Rate_Percentage DESC;


-- 17. Which geography has the lowest churn rate?

SELECT TOP 1
    Geography,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY Geography
ORDER BY Churn_Rate_Percentage ASC;


-- 18. What is the churn rate by gender?

SELECT
    Gender,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY Gender
ORDER BY Churn_Rate_Percentage DESC;


-- 19. Which gender has the highest churn rate?

SELECT TOP 1
    Gender,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY Gender
ORDER BY Churn_Rate_Percentage DESC;


-- 20. What is the average age of customers by geography?

SELECT
    Geography,
    ROUND(AVG(Age), 2) AS Average_Age
FROM churn
GROUP BY Geography
ORDER BY Average_Age DESC;



-- ================================================================
-- C. AGE & TENURE ANALYSIS — QUESTIONS 21–30
-- ================================================================

-- 21. What is the average age of churned customers compared with retained customers?
-- Exited = 0 → Retained
-- Exited = 1 → Churned

SELECT
    Exited,
    COUNT(*) AS Total_Customers,
    ROUND(AVG(Age), 2) AS Average_Age
FROM churn
GROUP BY Exited
ORDER BY Exited;


-- 22. What is the churn rate for each age group?

SELECT
    AgeGroup,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY AgeGroup
ORDER BY Churn_Rate_Percentage DESC;


-- 23. Which age group has the highest churn rate?

SELECT TOP 1
    AgeGroup,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY AgeGroup
ORDER BY Churn_Rate_Percentage DESC;


-- 24. Which age group has the lowest churn rate?

SELECT TOP 1
    AgeGroup,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY AgeGroup
ORDER BY Churn_Rate_Percentage ASC;


-- 25. How many customers are in each age group?

SELECT
    AgeGroup,
    COUNT(*) AS Total_Customers
FROM churn
GROUP BY AgeGroup
ORDER BY Total_Customers DESC;


-- 26. How many churned customers belong to each age group?

SELECT
    AgeGroup,
    SUM(Exited) AS Churned_Customers
FROM churn
GROUP BY AgeGroup
ORDER BY Churned_Customers DESC;


-- 27. What is the average tenure of churned customers
--     versus retained customers?

SELECT
    Exited,
    COUNT(*) AS Total_Customers,
    ROUND(AVG(Tenure), 2) AS Average_Tenure
FROM churn
GROUP BY Exited
ORDER BY Exited;


-- 28. What is the churn rate for each tenure year?

SELECT
    Tenure,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY Tenure
ORDER BY Tenure;


-- 29. Which tenure group has the highest churn rate?

SELECT TOP 1
    Tenure,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY Tenure
ORDER BY Churn_Rate_Percentage DESC;


-- 30. Which tenure group has the lowest churn rate?

SELECT TOP 1
    Tenure,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY Tenure
ORDER BY Churn_Rate_Percentage ASC;



-- ================================================================
-- D. CUSTOMER PRODUCT & ENGAGEMENT ANALYSIS — QUESTIONS 31–40
-- ================================================================

-- 31. How many customers have each number of products?

SELECT
    NumOfProducts,
    COUNT(*) AS Total_Customers
FROM churn
GROUP BY NumOfProducts
ORDER BY NumOfProducts;


-- 32. What is the churn rate by number of products?

SELECT
    NumOfProducts,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY NumOfProducts
ORDER BY Churn_Rate_Percentage DESC;


-- 33. Which product-count segment has the highest churn rate?

SELECT TOP 1
    NumOfProducts,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY NumOfProducts
ORDER BY Churn_Rate_Percentage DESC;


-- 34. Which product-count segment has the lowest churn rate?

SELECT TOP 1
    NumOfProducts,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY NumOfProducts
ORDER BY Churn_Rate_Percentage ASC;


-- 35. How many customers have a credit card?

SELECT
    HasCrCard,
    COUNT(*) AS Total_Customers
FROM churn
GROUP BY HasCrCard;


-- 36. What percentage of customers have a credit card?

SELECT
    CAST(SUM(HasCrCard) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Credit_Card_Percentage
FROM churn;


-- 37. What is the churn rate for customers with and without a credit card?

SELECT
    HasCrCard,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY HasCrCard
ORDER BY Churn_Rate_Percentage DESC;


-- 38. How many customers are active versus inactive members?

SELECT
    IsActiveMember,
    COUNT(*) AS Total_Customers
FROM churn
GROUP BY IsActiveMember;


-- 39. What is the churn rate for active versus inactive members?

SELECT
    IsActiveMember,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY IsActiveMember
ORDER BY Churn_Rate_Percentage DESC;


-- 40. How much higher is the churn rate among inactive members compared with active members?

SELECT
    (SELECT
        CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*)
     FROM churn
     WHERE IsActiveMember = 0) AS Inactive_Churn_Rate,
    (SELECT
        CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*)
     FROM churn
     WHERE IsActiveMember = 1)
        AS Active_Churn_Rate;



-- ================================================================
-- E. FINANCIAL & CREDIT ANALYSIS — QUESTIONS 41–50
-- ================================================================

-- 41. What is the average credit score of churned versus retained customers?

SELECT
    Exited,
    COUNT(*) AS Total_Customers,
    ROUND(AVG(CreditScore), 2) AS Average_Credit_Score
FROM churn
GROUP BY Exited
ORDER BY Exited;


-- 42. What is the churn rate by credit-score band?

SELECT
    CreditScoreBand,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY CreditScoreBand
ORDER BY Churn_Rate_Percentage DESC;


-- 43. Which credit-score band has the highest churn rate?

SELECT TOP 1
    CreditScoreBand,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY CreditScoreBand
ORDER BY Churn_Rate_Percentage DESC;


-- 44. What is the average balance of churned
--     versus retained customers?

SELECT
    Exited,
    COUNT(*) AS Total_Customers,
    ROUND(AVG(Balance), 2) AS Average_Balance
FROM churn
GROUP BY Exited
ORDER BY Exited;


-- 45. What is the churn rate by balance band?

SELECT
    BalanceBand,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY BalanceBand
ORDER BY Churn_Rate_Percentage DESC;


-- 46. Which balance band has the highest churn rate?

SELECT TOP 1
    BalanceBand,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY BalanceBand
ORDER BY Churn_Rate_Percentage DESC;


-- 47. What is the average estimated salary of churned versus retained customers?

SELECT
    Exited,
    COUNT(*) AS Total_Customers,
    ROUND(AVG(EstimatedSalary), 2) AS Average_Estimated_Salary
FROM churn
GROUP BY Exited
ORDER BY Exited;


-- 48. What is the churn rate by estimated-salary band?

SELECT
    CASE
        WHEN EstimatedSalary < 50000 THEN 'Below 50K'
        WHEN EstimatedSalary < 100000 THEN '50K - 100K'
        WHEN EstimatedSalary < 150000 THEN '100K - 150K'
        ELSE '150K+'
    END AS Salary_Band,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY
    CASE
        WHEN EstimatedSalary < 50000 THEN 'Below 50K'
        WHEN EstimatedSalary < 100000 THEN '50K - 100K'
        WHEN EstimatedSalary < 150000 THEN '100K - 150K'
        ELSE '150K+'
    END
ORDER BY Churn_Rate_Percentage DESC;


-- 49. Which salary band has the highest churn rate?

SELECT TOP 1
   CASE
        WHEN EstimatedSalary < 50000 THEN 'Below 50K'
        WHEN EstimatedSalary < 100000 THEN '50K - 100K'
        WHEN EstimatedSalary < 150000 THEN '100K - 150K'
        ELSE '150K+'
    END AS Salary_Band,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*)
        AS Churn_Rate_Percentage
FROM churn
GROUP BY
    CASE
        WHEN EstimatedSalary < 50000 THEN 'Below 50K'
        WHEN EstimatedSalary < 100000 THEN '50K - 100K'
        WHEN EstimatedSalary < 150000 THEN '100K - 150K'
        ELSE '150K+'
    END
ORDER BY Churn_Rate_Percentage DESC;

-- 50. What percentage of customers have a zero account balance, and what is their churn rate?

SELECT
    CASE
        WHEN Balance = 0 THEN 'Zero Balance'
        ELSE 'Non-Zero Balance'
    END AS Balance_Status,
    COUNT(*) AS Total_Customers,
    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM churn) AS Customer_Percentage,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) AS Churn_Rate_Percentage
FROM churn
GROUP BY
    CASE
        WHEN Balance = 0 THEN 'Zero Balance'
        ELSE 'Non-Zero Balance'
    END;



-- ================================================================
-- F. GEOGRAPHY + BEHAVIOUR ANALYSIS — QUESTIONS 51–57
-- ================================================================

-- 51. What is the churn rate by geography and gender?

SELECT
    Geography,
    Gender,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*)
        AS Churn_Rate_Percentage
FROM churn
GROUP BY Geography, Gender
ORDER BY Churn_Rate_Percentage DESC;


-- 52. Which geography-gender combination has the highest churn rate?

SELECT TOP 1
    Geography,
    Gender,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*)
        AS Churn_Rate_Percentage
FROM churn
GROUP BY Geography, Gender
ORDER BY Churn_Rate_Percentage DESC;


-- 53. What is the churn rate by geography and active membership status?

SELECT
    Geography,
    IsActiveMember,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*)
        AS Churn_Rate_Percentage
FROM churn
GROUP BY Geography, IsActiveMember
ORDER BY Churn_Rate_Percentage DESC;


-- 54. Which geography has the highest churn rate among inactive members?

SELECT TOP 1
    Geography,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*)
        AS Churn_Rate_Percentage
FROM churn
WHERE IsActiveMember = 0
GROUP BY Geography
ORDER BY Churn_Rate_Percentage DESC;


-- 55. What is the churn rate by geography and number of products?

SELECT
    Geography,
    NumOfProducts,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*)
        AS Churn_Rate_Percentage
FROM churn
GROUP BY Geography, NumOfProducts
ORDER BY Churn_Rate_Percentage DESC;


-- 56. Which geography-product combination has the highest churn rate?

SELECT TOP 1
    Geography,
    NumOfProducts,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*)
        AS Churn_Rate_Percentage
FROM churn
GROUP BY Geography, NumOfProducts
ORDER BY Churn_Rate_Percentage DESC;


-- 57. What is the churn rate by age group and active membership status?

SELECT
    AgeGroup,
    IsActiveMember,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*)
        AS Churn_Rate_Percentage
FROM churn
GROUP BY AgeGroup, IsActiveMember
ORDER BY Churn_Rate_Percentage DESC;



-- ================================================================
-- G. CUSTOMER RISK ANALYSIS — QUESTIONS 58–63
-- ================================================================

-- 58. Which customers have the highest combination of age, balance and churn risk?
-- We focus on older customers with high balances who have already churned.

SELECT TOP 20
    CustomerId,
    Age,
    Balance,
    Exited
FROM churn
WHERE Exited = 1
ORDER BY Age DESC, Balance DESC;


-- 59. What percentage of customers are both inactive members and churned?

SELECT
    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM churn)
        AS Inactive_Churned_Percentage
FROM churn
WHERE IsActiveMember = 0
  AND Exited = 1;


-- 60. What percentage of customers are inactive members with only one product?

SELECT
    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM churn)
        AS Inactive_One_Product_Percentage
FROM churn
WHERE IsActiveMember = 0
  AND NumOfProducts = 1;


-- 61. Which age group has the highest churn rate among inactive members?

SELECT TOP 1
    AgeGroup,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*)
        AS Churn_Rate_Percentage
FROM churn
WHERE IsActiveMember = 0
GROUP BY AgeGroup
ORDER BY Churn_Rate_Percentage DESC;


-- 62. Which customer segment has a churn rate above the overall 20.37% benchmark?

SELECT
    Geography,
    AgeGroup,
    IsActiveMember,
    NumOfProducts,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*)
        AS Churn_Rate_Percentage
FROM churn
GROUP BY
    Geography,
    AgeGroup,
    IsActiveMember,
    NumOfProducts
HAVING
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) > 20.37
ORDER BY Churn_Rate_Percentage DESC;


-- 63. Which combinations of geography, age group, activity status and number of products have the highest churn rates?

SELECT
    Geography,
    AgeGroup,
    IsActiveMember,
    NumOfProducts,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*)
        AS Churn_Rate_Percentage
FROM churn
GROUP BY
    Geography,
    AgeGroup,
    IsActiveMember,
    NumOfProducts
HAVING COUNT(*) >= 30
ORDER BY Churn_Rate_Percentage DESC;



-- ================================================================
-- H. ADVANCED SQL & CUSTOMER SEGMENTATION — QUESTIONS 64–67
-- ================================================================

-- 64. Rank the geographies by customer churn rate using RANK().

SELECT
    Geography,
    COUNT(*) AS Total_Customers,
    SUM(Exited) AS Churned_Customers,
    CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*)
        AS Churn_Rate_Percentage,
    RANK() OVER (ORDER BY CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*) DESC ) AS Churn_Rank
FROM churn
GROUP BY Geography
ORDER BY Churn_Rank;


-- 65. Rank customer segments by churn rate
--     using a CTE and window functions.

WITH Customer_Segments AS
(
    SELECT
        Geography,
        AgeGroup,
        IsActiveMember,
        NumOfProducts,
        COUNT(*) AS Total_Customers,
        SUM(Exited) AS Churned_Customers,
        CAST(SUM(Exited) AS DECIMAL(10,2)) * 100.0 / COUNT(*)
            AS Churn_Rate_Percentage
    FROM churn
    GROUP BY
        Geography,
        AgeGroup,
        IsActiveMember,
        NumOfProducts
    HAVING COUNT(*) >= 30
)
SELECT
    Geography,
    AgeGroup,
    IsActiveMember,
    NumOfProducts,
    Total_Customers,
    Churned_Customers,
    Churn_Rate_Percentage,
     RANK() OVER (ORDER BY Churn_Rate_Percentage DESC) AS Segment_Rank
FROM Customer_Segments
ORDER BY Segment_Rank;


-- 66. Identify customers whose characteristics place them
--     in a high-churn segment.
-- High-churn characteristics:  Older customers + inactive membership + multiple products.

SELECT
    CustomerId,
    Age,
    Geography,
    IsActiveMember,
    NumOfProducts,
    Exited
FROM churn
WHERE Age >= 50
  AND IsActiveMember = 0
  AND NumOfProducts >= 2
ORDER BY Age DESC;


-- 67. Create a comprehensive customer-risk segmentation that classifies customers into Low, Medium and High
--     Churn Risk based on multiple characteristics.

SELECT
    CustomerId,
    Geography,
    Age,
    IsActiveMember,
    NumOfProducts,
    Balance,
    Exited,
    CASE
        WHEN Exited = 1 THEN 'High Risk'
        WHEN IsActiveMember = 0 AND Age >= 50 THEN 'High Risk'
        WHEN IsActiveMember = 0 AND NumOfProducts >= 2 THEN 'High Risk'
        WHEN Age >= 50 OR IsActiveMember = 0 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS Churn_Risk
FROM churn
ORDER BY
    Churn_Risk,
    Age DESC;

