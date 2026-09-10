-- Business Question: How well are newly acquired customers being retained over time?
-- Performs cohort retention analysis.
-- Cohort = month of first observed purchase.

WITH customer_cohorts AS (
    -- Determine the first purchase month for each customer
    SELECT 
        customer_id,
        DATE_TRUNC('month', MIN(transaction_timestamp)) AS cohort_month
    FROM transactions
    GROUP BY customer_id
),
customer_activities AS (
    -- Determine all months where a customer made a purchase
    SELECT DISTINCT
        customer_id,
        DATE_TRUNC('month', transaction_timestamp) AS activity_month
    FROM transactions
),
cohort_retention AS (
    -- Join cohort with activity to calculate months since first purchase
    SELECT 
        c.cohort_month,
        a.activity_month,
        c.customer_id,
        EXTRACT(YEAR FROM age(a.activity_month, c.cohort_month)) * 12 + 
        EXTRACT(MONTH FROM age(a.activity_month, c.cohort_month)) AS months_since_first_purchase
    FROM customer_cohorts c
    JOIN customer_activities a ON c.customer_id = a.customer_id
),
cohort_sizes AS (
    -- Calculate the total size of each cohort (Month 0)
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_size
    FROM customer_cohorts
    GROUP BY cohort_month
)
-- Aggregate to calculate retention rate
SELECT 
    r.cohort_month::DATE AS cohort_month,
    s.cohort_size,
    r.months_since_first_purchase,
    COUNT(DISTINCT r.customer_id) AS retained_customers,
    ROUND((COUNT(DISTINCT r.customer_id)::NUMERIC / s.cohort_size::NUMERIC) * 100, 2) AS retention_rate_pct
FROM cohort_retention r
JOIN cohort_sizes s ON r.cohort_month = s.cohort_month
GROUP BY 
    r.cohort_month, 
    s.cohort_size, 
    r.months_since_first_purchase
ORDER BY 
    r.cohort_month, 
    r.months_since_first_purchase;
