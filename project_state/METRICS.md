# Performance Metrics

## Dataset
- Customers: 10,000
- Products: 500
- Transactions: 245,210
- Date range: 2024-07-01 to 2026-06-30
- Segment distribution: Champion 10%, Loyal 20%, New 20%, At Risk 25%, Lost 25%

## CSV File Sizes
- customers.csv: 519 KB
- products.csv: 17 KB
- transactions.csv: 18.6 MB

## Generation Performance
- Generation time: 30.97s
- Validation time: 0.21s

## Data Validation
- Checks passed: 50/50
- Reproducibility: PASS (MD5 match)

## Database Load
- Provisioning method: Portable user-space PostgreSQL binary
- PostgreSQL version: 16.4
- Load time: ~8.37s total (COPY)
- Schema creation: < 0.1s
- Total loaded transactions: 245,210
- Total revenue loaded: $53,581,128.12
- Indexes created: 3 (transaction_timestamp, customer_id, product_id)

## Query Performance
- Baseline execution time (customer_metrics.sql): ~230 ms
- Optimized execution time (customer_metrics.sql): ~139 ms (39% improvement)
- Baseline planning time (customer_metrics.sql): ~2.2 ms
- Baseline scan type (customer_metrics.sql): Seq Scan + Hash Right Join
- Optimized planning time (customer_metrics.sql): ~0.6 ms
- Optimized scan type (customer_metrics.sql): Parallel Partial HashAggregate + Hash Left Join
- Baseline execution time (rfm.sql): ~168 ms
- Optimized execution time (rfm.sql): No change (Seq Scan proven optimal)

## Analytical Metrics
- Total Revenue: $53,581,128.12
- Total Transactions: 245,210
- Active Customers: 10,000
- Average Order Value (AOV): $218.51
- Repeat Purchase Rate: 100.00%
- Revenue Concentration (Top 1%): 4.67%
- Revenue Concentration (Top 20%): 18.02%
- Top Category by Revenue: Electronics ($22,476,227.63)

## Python Analytics Layer
- Number of analytical datasets: 9 (Overall KPIs, TS KPIs, Customer Metrics, RFM, Raw Cohorts, Heatmap Cohorts, Categories, Concentration, Top Customers)
- Validation tests passed: 8/8
- Python processing and test duration: ~1.1 - 2.5 seconds

## Deployment
- Dashboard startup time: ~4 seconds (local headless)
- Number of dashboard sections: 8 (KPIs, Trend, Category, RFM, Cohorts, Concentration, Top Customers, Explorer)
- Analytics datasets consumed: 9
- Status: BLOCKED (Missing cloud database credentials in the development environment)
- URL: N/A
- Public smoke-test result: N/A
- Final automated-test result: PASS (Local test suite passes perfectly)

## Plan Compliance
- Phase 0: PASS
- Phase 1: PASS
- Phase 2: PASS
- Phase 3: PASS
- Phase 4: PASS
- Phase 5: PASS
- Phase 6: PASS
- Phase 7: PARTIAL (Finalization completed; Public deployment blocked)
