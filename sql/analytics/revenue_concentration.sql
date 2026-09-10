-- Business Question: How dependent is revenue on the highest-value customers?
-- Calculates the share of total revenue contributed by the Top 1%, 5%, 10%, and 20% of customers.

WITH customer_revenue AS (
    SELECT 
        customer_id,
        SUM(amount) AS total_spend
    FROM transactions
    GROUP BY customer_id
),
ranked_customers AS (
    SELECT 
        customer_id,
        total_spend,
        PERCENT_RANK() OVER (ORDER BY total_spend DESC) AS spend_percentile,
        SUM(total_spend) OVER () AS global_total_revenue
    FROM customer_revenue
),
concentration_bands AS (
    SELECT 
        customer_id,
        CASE 
            WHEN spend_percentile <= 0.01 THEN 'Top 1%'
            WHEN spend_percentile <= 0.05 THEN 'Top 5%'
            WHEN spend_percentile <= 0.10 THEN 'Top 10%'
            WHEN spend_percentile <= 0.20 THEN 'Top 20%'
            ELSE 'Rest'
        END AS customer_band,
        total_spend,
        global_total_revenue,
        -- Need numeric percentile for ordering
        CASE 
            WHEN spend_percentile <= 0.01 THEN 1
            WHEN spend_percentile <= 0.05 THEN 5
            WHEN spend_percentile <= 0.10 THEN 10
            WHEN spend_percentile <= 0.20 THEN 20
            ELSE 100
        END AS band_order
    FROM ranked_customers
)
SELECT 
    customer_band,
    COUNT(customer_id) AS customer_count,
    SUM(total_spend) AS band_revenue,
    MAX(global_total_revenue) AS total_revenue,
    ROUND((SUM(total_spend) / MAX(global_total_revenue)) * 100, 2) AS pct_of_total_revenue
FROM concentration_bands
GROUP BY customer_band, band_order
ORDER BY band_order;
