-- Business Question: Who are our customers and what is their overall value and behavior?
-- Creates a reusable customer-level aggregation table/CTE.
-- PHASE_4_CANDIDATE: customer revenue aggregation (aggregating large transaction history to customer level)

WITH t_agg AS (
    SELECT 
        customer_id,
        COUNT(transaction_id) AS transaction_count,
        SUM(amount) AS total_revenue,
        MIN(transaction_timestamp) AS min_ts,
        MAX(transaction_timestamp) AS max_ts
    FROM transactions
    GROUP BY customer_id
)
SELECT 
    c.customer_id,
    c.signup_date,
    c.city,
    c.age_group,
    c.gender,
    c.acquisition_channel,
    COALESCE(t.transaction_count, 0) AS transaction_count,
    COALESCE(t.total_revenue, 0) AS total_revenue,
    COALESCE(t.total_revenue / NULLIF(t.transaction_count, 0), 0) AS average_order_value,
    t.min_ts::DATE AS first_purchase_date,
    t.max_ts::DATE AS last_purchase_date,
    EXTRACT(DAY FROM (
        (SELECT MAX(transaction_timestamp) FROM transactions) - t.max_ts
    )) AS days_since_last_purchase,
    CASE 
        WHEN t.transaction_count > 1 
        THEN EXTRACT(DAY FROM (t.max_ts - t.min_ts)) / (t.transaction_count - 1)
        ELSE NULL 
    END AS purchase_frequency_days
FROM customers c
LEFT JOIN t_agg t ON c.customer_id = t.customer_id
ORDER BY t.total_revenue DESC NULLS LAST;
