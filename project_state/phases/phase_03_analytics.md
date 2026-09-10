# Phase 03 — Analytical SQL & Business Insights

Status: COMPLETE

Objective: Build the core analytical SQL layer to answer business questions regarding revenue, customers, segmentation, and cohorts using PostgreSQL.

Resource prompt: resources/prompts/PHASE_03_ANALYTICS.md

Implementation-plan requirements:
- [x] Create KPI queries (revenue, customers, AOV, repeat purchase)
- [x] Create customer-level aggregation metrics
- [x] Implement RFM segmentation (derived independently from transactions)
- [x] Create cohort retention analysis (by signup/first-purchase month)
- [x] Analyze revenue by product category
- [x] Calculate revenue concentration (Top 1%, 5%, 10%, 20%)
- [x] Frame all SQL files around specific business questions
- [x] Execute and validate all queries in PostgreSQL

Inputs: 
- Phase 2 PostgreSQL Database tables (customers, products, transactions)

Outputs:
- sql/analytics/kpis.sql
- sql/analytics/customer_metrics.sql
- sql/analytics/rfm.sql
- sql/analytics/cohorts.sql
- sql/analytics/category_analysis.sql
- sql/analytics/revenue_concentration.sql
- sql/analytics/top_customers.sql
- tests/test_analytics.py

Validation: PASS
- **Join Integrity**: Verified that joining transactions to dimensions (customers, products) preserves exact transaction row counts.
- **Revenue Conservation**: RFM revenue sum and Category revenue sum reconcile perfectly with global total revenue ($53,581,128.12).
- **Concentration**: Tested percentiles and cumulative revenue successfully. 

Plan compliance: PASS

Actual metrics:
- Total Revenue: $53,581,128.12
- Total Transactions: 245,210
- Active Customers: 10,000
- AOV: $218.51
- Repeat Purchase Rate: 100.00%
- Revenue Concentration: Top 1% = 4.67%, Top 5% = 12.24%, Top 20% = 18.02%
- Top Category: Electronics ($22,476,227.63)

Phase 4 Candidate Workloads:
1. **RFM Segmentation (`rfm.sql`)**: Uses multiple heavy window functions (`NTILE(5)`) over aggregated transaction groupings. Ideal for EXPLAIN ANALYZE tuning.
2. **Customer Metrics (`customer_metrics.sql`)**: Deep aggregations and multiple date calculations joining the large transaction table.

Next phase: PHASE_04_PERFORMANCE (resources/prompts/PHASE_04_PERFORMANCE.md)

Resume instructions:
1. Ensure the database server is running (`pg_ctl start`).
2. Read project_state/STATE.md and resources/IMPLEMENTATION_PLAN.md.
3. Follow instructions in resources/prompts/PHASE_04_PERFORMANCE.md.
