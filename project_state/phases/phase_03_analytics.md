# Phase 03 — Analytics

Status: NOT_STARTED

Objective: Implement KPI queries, RFM segmentation, cohort retention, customer/category analysis, revenue concentration.

Resource prompt: resources/prompts/PHASE_03_ANALYTICS.md

Implementation-plan requirements:
- sql/kpi_queries.sql (revenue, active customers, AOV, repeat rate, monthly trend)
- sql/rfm.sql (R/F/M scores, segment mapping, documented rules)
- sql/retention.sql (cohort month, months since acquisition, retention rate)
- sql/customer_analysis.sql (category breakdown, revenue concentration)
- src/analytics.py (Python wrapper returning DataFrames)

Inputs: Populated PostgreSQL database

Outputs:
- sql/kpi_queries.sql
- sql/rfm.sql
- sql/retention.sql
- sql/customer_analysis.sql
- src/analytics.py

Implementation: Not started

Validation: Not started

Plan compliance: Not started

Problems: None

Decisions: None yet

Metrics: None yet

Known limitations: None yet

Next phase: PHASE_04_PERFORMANCE

Resume instructions: Read STATE.md, then this file, then the phase prompt.
