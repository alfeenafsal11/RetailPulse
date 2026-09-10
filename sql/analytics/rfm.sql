-- Business Question: Which customers are Champions, Loyal, At Risk, or Lost based on observed purchase behavior?
-- Performs RFM (Recency, Frequency, Monetary) segmentation using PostgreSQL window functions (NTILE).
-- PHASE_4_CANDIDATE: RFM segmentation (window functions over aggregated transaction data)

WITH customer_rfm_raw AS (
    SELECT 
        customer_id,
        MAX(transaction_timestamp)::DATE AS last_purchase_date,
        -- Recency: Days since last purchase (lower is better)
        EXTRACT(DAY FROM (
            (SELECT MAX(transaction_timestamp) FROM transactions) - MAX(transaction_timestamp)
        )) AS recency_days,
        -- Frequency: Total number of transactions (higher is better)
        COUNT(transaction_id) AS frequency,
        -- Monetary: Total amount spent (higher is better)
        SUM(amount) AS monetary
    FROM transactions
    GROUP BY customer_id
),
rfm_scores AS (
    SELECT 
        customer_id,
        recency_days,
        frequency,
        monetary,
        -- Recency Score: 5 is most recent, 1 is least recent
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
        -- Frequency Score: 5 is most frequent, 1 is least frequent
        NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
        -- Monetary Score: 5 is highest spend, 1 is lowest spend
        NTILE(5) OVER (ORDER BY monetary ASC) AS m_score
    FROM customer_rfm_raw
),
rfm_segments AS (
    SELECT 
        customer_id,
        recency_days,
        frequency,
        monetary,
        r_score,
        f_score,
        m_score,
        -- Segmentation Logic:
        -- Champions: Bought recently, buy often and spend the most
        -- Loyal: Spend good money and often, responsive to promotions
        -- New: Bought recently, but not often
        -- At Risk: Spent big money and purchased often but long time ago
        -- Lost: Lowest recency, frequency and monetary scores
        CASE
            WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
            WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Loyal'
            WHEN r_score >= 4 AND f_score <= 2 THEN 'New'
            WHEN r_score <= 2 AND f_score >= 3 AND m_score >= 3 THEN 'At Risk'
            WHEN r_score <= 2 AND f_score <= 2 AND m_score <= 2 THEN 'Lost'
            ELSE 'Other' -- Catch-all for middle-tier customers
        END AS rfm_segment
    FROM rfm_scores
)
-- Output summary for business insight
SELECT 
    rfm_segment,
    COUNT(customer_id) AS segment_size,
    SUM(monetary) AS total_revenue,
    AVG(monetary) AS avg_revenue_per_customer,
    SUM(frequency) AS total_transactions,
    AVG(recency_days) AS avg_recency_days,
    AVG(frequency) AS avg_frequency
FROM rfm_segments
GROUP BY rfm_segment
ORDER BY total_revenue DESC;
