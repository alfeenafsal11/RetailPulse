# PHASE 03 — Analytical SQL

## Objective

Implement the core analytical SQL queries: KPIs, RFM segmentation, cohort retention, customer/category analysis, and revenue concentration. Wrap these in a Python analytics layer.

## Scope

- SQL query files for all analytical requirements
- Python analytics module to execute and return query results
- Validation of query results

## Inputs

- Populated PostgreSQL database from Phase 2
- `resources/IMPLEMENTATION_PLAN.md` — analytical SQL requirements, RFM methodology, cohort methodology

## Required Implementation Tasks

1. Create `sql/kpi_queries.sql`:
   - Total revenue: SUM(amount)
   - Active customers: COUNT(DISTINCT customer_id) in analysis period
   - Average order value: total_revenue / transaction_count
   - Repeat purchase rate: customers_with_≥2 / customers_with_≥1
   - Monthly revenue trend

2. Create `sql/rfm.sql`:
   - Calculate raw Recency, Frequency, Monetary per customer
   - Score each dimension 1–5 using NTILE(5)
   - Map (R, F, M) scores to segments using documented rules
   - Segment labels: Champions, Loyal Customers, Potential Loyalists, At Risk, Lost, New Customers
   - Document segmentation rules in SQL comments

3. Create `sql/retention.sql`:
   - Determine each customer's cohort month (signup or first purchase month)
   - Calculate activity in subsequent months
   - Output: cohort_month, months_since_acquisition, customer_count, retention_rate
   - Validate Month 0 retention ≈ 100%

4. Create `sql/customer_analysis.sql`:
   - Revenue by category
   - Transactions by category
   - AOV by category
   - Customers by category
   - Revenue concentration: Top 1%, 5%, 10%, 20% customer contribution

5. Create/update `src/analytics.py`:
   - Python functions wrapping each SQL query
   - Return results as Pandas DataFrames
   - Use parameterized queries where applicable
   - Document each function

## Required Files

```
sql/kpi_queries.sql
sql/rfm.sql
sql/retention.sql
sql/customer_analysis.sql
src/analytics.py
```

## Validation Checks

- [ ] All SQL files execute without errors
- [ ] KPI values are reasonable (positive revenue, AOV > 0, repeat rate 0–1)
- [ ] RFM assigns every customer exactly one segment
- [ ] All 6 segments are represented in RFM results
- [ ] Cohort retention Month 0 ≈ 100%
- [ ] Retention rates decrease over time (general trend)
- [ ] Revenue concentration sums are ≤ total revenue
- [ ] Category analysis covers all product categories
- [ ] analytics.py functions return valid DataFrames

## Expected Outputs

- Four SQL query files
- Python analytics layer
- Validated analytical results

## Definition of Done

All four SQL files execute correctly against the database. RFM assigns every customer a segment. Cohort retention matrix is valid. Revenue concentration and category analysis return meaningful results. Python analytics layer wraps all queries.

## Handoff Requirements

- All SQL queries verified
- Sample results documented or captured
- analytics.py ready for Streamlit integration in Phase 5
- STATE.md updated

## STOP INSTRUCTION

**Do NOT execute PHASE 4 after completing PHASE 3.**

Stop after producing the Phase 3 completion report. Wait for explicit user instruction to proceed.
