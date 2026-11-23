-- Loyalty proxy segmentation by tenure (no transaction data available for RFM)
-- Table: COCO_ANALYST.MY_TABLE.DIM_CUSTOMERS

-- 1. Confirm columns
DESCRIBE TABLE COCO_ANALYST.MY_TABLE.DIM_CUSTOMERS;

-- 2. Tenure quintiles (5 = longest tenure = "Loyal")
WITH t AS (
    SELECT CUSTOMER_ID, COUNTRY, SUBSCRIPTION_DATE,
           DATEDIFF('day', SUBSCRIPTION_DATE, CURRENT_DATE) AS tenure_days,
           NTILE(5) OVER (ORDER BY SUBSCRIPTION_DATE DESC) AS tenure_score
    FROM COCO_ANALYST.MY_TABLE.DIM_CUSTOMERS
    WHERE SUBSCRIPTION_DATE IS NOT NULL
)
SELECT tenure_score,
       CASE tenure_score WHEN 5 THEN 'Loyal (longest tenure)' WHEN 4 THEN 'Established'
            WHEN 3 THEN 'Mid' WHEN 2 THEN 'Recent' ELSE 'New' END AS segment,
       COUNT(*) AS customers,
       ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct,
       MIN(SUBSCRIPTION_DATE) AS earliest, MAX(SUBSCRIPTION_DATE) AS latest,
       ROUND(AVG(tenure_days)) AS avg_tenure_days
FROM t GROUP BY 1, 2 ORDER BY 1 DESC;

-- 3. Loyal segment by country
WITH t AS (
    SELECT CUSTOMER_ID, COUNTRY, SUBSCRIPTION_DATE,
           NTILE(5) OVER (ORDER BY SUBSCRIPTION_DATE DESC) AS tenure_score
    FROM COCO_ANALYST.MY_TABLE.DIM_CUSTOMERS
    WHERE SUBSCRIPTION_DATE IS NOT NULL
)
SELECT COUNTRY, COUNT(*) AS loyal_customers
FROM t WHERE tenure_score = 5
GROUP BY 1 ORDER BY 2 DESC LIMIT 10;

-- 4. Longest-tenured customer IDs (IDs only, no PII)
SELECT CUSTOMER_ID, COUNTRY, SUBSCRIPTION_DATE
FROM COCO_ANALYST.MY_TABLE.DIM_CUSTOMERS
WHERE SUBSCRIPTION_DATE IS NOT NULL
ORDER BY SUBSCRIPTION_DATE, CUSTOMER_ID LIMIT 10;
