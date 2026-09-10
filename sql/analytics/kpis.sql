-- Business Question: How is the retail business performing overall?
-- Calculates core retail KPIs: Total Revenue, Customers, Transactions, Average Order Value (AOV), and Repeat Purchase Rate.

WITH customer_stats AS (
    SELECT 
        customer_id,
        COUNT(transaction_id) as txn_count
    FROM transactions
    GROUP BY customer_id
),
overall_kpis AS (
    SELECT 
        SUM(amount) AS total_revenue,
        COUNT(DISTINCT customer_id) AS active_customers, -- Active = has at least 1 transaction in the period
        COUNT(transaction_id) AS total_transactions,
        SUM(amount) / COUNT(transaction_id) AS average_order_value
    FROM transactions
),
repeat_customers AS (
    SELECT 
        COUNT(customer_id) AS customers_with_multiple_purchases,
        (SELECT COUNT(customer_id) FROM customer_stats WHERE txn_count >= 1) AS total_active_customers
    FROM customer_stats
    WHERE txn_count > 1
)
SELECT 
    k.total_revenue,
    k.active_customers,
    k.total_transactions,
    k.average_order_value,
    (r.customers_with_multiple_purchases::FLOAT / NULLIF(r.total_active_customers, 0)) AS repeat_purchase_rate
FROM overall_kpis k
CROSS JOIN repeat_customers r;

-- Business Question: What is the time-series revenue trend?
-- Calculates revenue by month
SELECT 
    DATE_TRUNC('month', transaction_timestamp) AS txn_month,
    SUM(amount) AS monthly_revenue,
    COUNT(transaction_id) AS monthly_transactions
FROM transactions
GROUP BY 1
ORDER BY 1;
