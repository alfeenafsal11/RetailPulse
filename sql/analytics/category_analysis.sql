-- Business Question: Which product categories drive the most revenue and engagement?
-- Calculates revenue, transaction count, units sold, and AOV by category.

SELECT 
    p.category,
    SUM(t.amount) AS total_revenue,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.quantity) AS total_units_sold,
    SUM(t.amount) / COUNT(t.transaction_id) AS average_transaction_value
FROM transactions t
JOIN products p ON t.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;
