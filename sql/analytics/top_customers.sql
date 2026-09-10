-- Business Question: Who are the top 20 highest-value customers?
-- Identifies key individuals for high-value engagement or VIP programs.

SELECT 
    c.customer_id,
    c.city,
    c.age_group,
    SUM(t.amount) AS total_revenue,
    COUNT(t.transaction_id) AS transaction_count,
    SUM(t.amount) / COUNT(t.transaction_id) AS average_order_value,
    MAX(t.transaction_timestamp)::DATE AS last_purchase_date
FROM customers c
JOIN transactions t ON c.customer_id = t.customer_id
GROUP BY 
    c.customer_id,
    c.city,
    c.age_group
ORDER BY total_revenue DESC
LIMIT 20;
