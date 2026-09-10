# PostgreSQL Performance Benchmark Analysis

## Workload 1: Customer Metrics (`sql/analytics/customer_metrics.sql`)

**Business purpose**: Calculate customer-level statistics (revenue, AOV, purchase dates, frequency) by joining dimension data (`customers`) with fact data (`transactions`).

**Baseline SQL**:
```sql
SELECT 
    c.customer_id, ...,
    COUNT(t.transaction_id) AS transaction_count,
    SUM(t.amount) AS total_revenue
FROM customers c
LEFT JOIN transactions t ON c.customer_id = t.customer_id
GROUP BY c.customer_id, ...
ORDER BY total_revenue DESC;
```

**Baseline Execution Time**: ~230 ms
**Planning Time**: ~0.5 - 2.2 ms

**Execution Plan Observations**:
- **Access path**: Sequential Scan on `transactions` (cost=0..5364.10) taking ~21ms.
- **Join strategy**: Hash Right Join. The planner creates a Hash table of the 10,000 customers (taking ~4ms) and then probes it with the 245,210 rows from the sequential scan (taking ~126ms).
- **Aggregation**: A massive HashAggregate then groups the 245,210 joined rows back down to 10,000 rows (taking ~220ms cumulative).

**Observed Bottleneck**: 
The query joins the 245,210 raw transactions with the `customers` table *before* aggregating. This causes the Hash Join and subsequent HashAggregate to process a very high cardinality of rows.

**Optimization Hypothesis**:
Pre-aggregating the `transactions` table into a CTE before the `LEFT JOIN` will dramatically reduce the join cardinality (from 245,210 down to 10,000), reducing memory and CPU overhead.

**Optimized SQL**:
```sql
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
SELECT c.customer_id, ..., t.transaction_count, t.total_revenue ...
FROM customers c
LEFT JOIN t_agg t ON c.customer_id = t.customer_id
ORDER BY t.total_revenue DESC NULLS LAST;
```

**Optimized Execution Time**: ~139 ms (39% improvement)

**Result and Planner Decision**:
- The planner now performs a `Partial HashAggregate` on `transactions` in parallel using background workers.
- The join cardinality is reduced to 10,000 rows. The `Hash Left Join` takes only ~4ms (down from ~126ms).
- Overall execution time drops significantly. Correctness validated.

---

## Workload 2: RFM Segmentation (`sql/analytics/rfm.sql`)

**Business purpose**: Calculate Recency, Frequency, and Monetary scores for all customers across the entire dataset.

**Baseline SQL**:
```sql
WITH customer_rfm_raw AS (
    SELECT customer_id, MAX(transaction_timestamp) ..., COUNT(transaction_id) ..., SUM(amount) ...
    FROM transactions GROUP BY customer_id
), rfm_scores AS (
    SELECT ..., NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score ...
    FROM customer_rfm_raw
) ...
```

**Baseline Execution Time**: ~168 ms
**Planning Time**: ~5.8 ms

**Execution Plan Observations**:
- **Access path**: Sequential Scan on `transactions` taking ~27ms.
- **Aggregation**: HashAggregate down to 10,000 rows (taking ~130ms cumulative).
- **Sorting/Windowing**: Followed by 3 sequential `Sort` and `WindowAgg` operations for the `NTILE()` functions, each taking ~20-30ms.

**Observed Bottleneck**:
The bulk of the execution time is spent on the full table scan and aggregation. An index `idx_transactions_customer` exists. A naive assumption might be that an index scan would be faster.

**Optimization Hypothesis (Diagnostic Experiment)**:
Force PostgreSQL to use the existing `idx_transactions_customer` index by disabling Sequential Scans (`SET enable_seqscan = off;`) to observe if pre-sorted index reads speed up the aggregation via `GroupAggregate`.

**Experiment Execution Time (Index Scan)**: ~197 ms (Slower than Baseline)

**Result and Planner Decision**:
- When forced, the planner uses an `Index Scan` on `idx_transactions_customer`. The scan itself takes ~56ms (compared to 27ms for Seq Scan).
- The planner switches to `GroupAggregate` instead of `HashAggregate` because the index provides pre-sorted data. However, `GroupAggregate` takes ~155ms (cumulative), meaning the overall pipeline is slower than the `Seq Scan -> HashAggregate` pipeline.
- **Why**: Sequential scans read data blocks contiguously, which is highly I/O efficient for full table scans. Index scans cause random heap fetches. Because RFM requires processing the *entire* dataset without filtering, PostgreSQL rationally ignores the index and chooses the Sequential Scan.

**Conclusion**: The baseline is already optimal. Adding further single-column or composite indexes will not improve performance because the query requires a full dataset scan.
