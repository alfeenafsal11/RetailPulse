# Architectural Decisions

## ADR-001
Decision: Use PostgreSQL as the database
Reason: Strong SQL support, relevant to target role (Xeno AI-Native Data Analyst), supports EXPLAIN ANALYZE for performance analysis
Alternatives considered: SQLite
Why rejected: Less representative for the target role, limited analytical SQL features
Affected resources: resources/IMPLEMENTATION_PLAN.md, requirements.txt

## ADR-002
Decision: Use Streamlit as the web framework
Reason: Fastest route to a live analytical application, built-in caching, free cloud deployment
Alternatives considered: React + FastAPI
Why rejected: Excessive implementation time for current objective and timeline
Affected resources: resources/IMPLEMENTATION_PLAN.md, requirements.txt

### Phase 3

- **ADR-011: SQL Analytics Organization**
  - **Context**: Need to organize analytical SQL queries for business insight generation.
  - **Decision**: Created independent SQL files inside `sql/analytics/` corresponding to specific business questions (e.g. `kpis.sql`, `rfm.sql`, `cohorts.sql`).
  - **Consequences**: Queries are reusable, independently executable artifacts that serve as the foundation for the Phase 4 performance tuning and the future Python analytics layer.

- **ADR-012: Python-based SQL Validation**
  - **Context**: Need to validate the analytical SQL results against the database.
  - **Decision**: Created `tests/test_analytics.py` using `psycopg2` to programmatically execute all queries, print results, and assert invariant logic (e.g., revenue totals match).
  - **Consequences**: Provides automated, reproducible validation of the SQL analytics without requiring manual `psql` queries.

### Phase 4

- **ADR-013: Pre-aggregation Optimization for Customer Metrics**
  - **Context**: `customer_metrics.sql` took ~230ms because it joined 245k transactions with 10k customers before aggregating the results, causing a massive Hash Right Join and HashAggregate.
  - **Decision**: Rewrote the query to aggregate transactions into a CTE (reducing cardinality to 10k) before performing a Hash Left Join to the customers table.
  - **Consequences**: Execution time reduced to ~139ms (39% faster). Join cost dropped significantly.

### Phase 4

- **ADR-013: Pre-aggregation Optimization for Customer Metrics**
  - **Context**: `customer_metrics.sql` took ~230ms because it joined 245k transactions with 10k customers before aggregating the results, causing a massive Hash Right Join and HashAggregate.
  - **Decision**: Rewrote the query to aggregate transactions into a CTE (reducing cardinality to 10k) before performing a Hash Left Join to the customers table.
  - **Consequences**: Execution time reduced to ~139ms (39% faster). Join cost dropped significantly.

- **ADR-014: Seq Scan Preference for RFM Validation**
  - **Context**: `rfm.sql` (baseline ~168ms) calculates scores over the entire dataset. It uses a Sequential Scan despite the existence of an index on `customer_id`.
  - **Decision**: Disabled sequential scans in a diagnostic experiment, which forced an Index Scan taking ~197ms (slower). Documented that PostgreSQL correctly chose the Sequential Scan because reading contiguous blocks for a full table scan is more efficient than random index fetches.
  - **Consequences**: No new indexes were added for RFM; the baseline execution plan is demonstrably optimal. Allowed us to demonstrate a deep understanding of planner choices in `benchmark_analysis.md`.

### Phase 5

- **ADR-015: PostgreSQL Tuple Cursor vs Dict Cursor for pandas**
  - **Context**: pandas.read_sql requires standard tuple sequences to convert DBAPI2 cursors into DataFrames. The previous database config used `psycopg2.extras.RealDictCursor`.
  - **Decision**: Removed `RealDictCursor` from the analytics connection flow, defaulting to standard cursors.
  - **Consequences**: Resolved an explicit `ValueError` in pandas, enabling standard fast ingestion of query results while retaining the raw analytical SQL logic.

### Phase 5

- **ADR-015: PostgreSQL Tuple Cursor vs Dict Cursor for pandas**
  - **Context**: pandas.read_sql requires standard tuple sequences to convert DBAPI2 cursors into DataFrames. The previous database config used `psycopg2.extras.RealDictCursor`.
  - **Decision**: Removed `RealDictCursor` from the analytics connection flow, defaulting to standard cursors.
  - **Consequences**: Resolved an explicit `ValueError` in pandas, enabling standard fast ingestion of query results while retaining the raw analytical SQL logic.

- **ADR-016: Strict SQL/Python Separation**
  - **Context**: Need to determine what processing happens in Python versus SQL.
  - **Decision**: Python solely handles data retrieval via existing SQL files (preserving Phase 4 optimizations) and performs only presentation-layer transformations (e.g., pivoting cohorts into a 24x24 heatmap and type casting).
  - **Consequences**: Avoids duplicating massive HashAggregates in pandas. Ensures PostgreSQL remains the undisputed source of truth for the 245k transactions.

### Phase 6

- **ADR-017: Preservation of 6-Tier RFM Output**
  - **Context**: Phase 5 output analysis showed that `load_rfm()` outputs a 6-row summary instead of the expected 5 named segments.
  - **Decision**: Investigated the underlying `sql/analytics/rfm.sql` query. The 6th row is 'Other', a legitimate catch-all segment for middle-tier customers whose RFM scores do not meet the strict boundary constraints of Champions, Loyal, New, At Risk, or Lost. This row was intentionally retained rather than deleted in the presentation layer.
  - **Consequences**: The dashboard accurately represents all 10,000 customers in its RFM visualizations, ensuring revenue and customer count reconciliation.

### Phase 6

- **ADR-017: Preservation of 6-Tier RFM Output**
  - **Context**: Phase 5 output analysis showed that `load_rfm()` outputs a 6-row summary instead of the expected 5 named segments.
  - **Decision**: Investigated the underlying `sql/analytics/rfm.sql` query. The 6th row is 'Other', a legitimate catch-all segment for middle-tier customers whose RFM scores do not meet the strict boundary constraints of Champions, Loyal, New, At Risk, or Lost. This row was intentionally retained rather than deleted in the presentation layer.
  - **Consequences**: The dashboard accurately represents all 10,000 customers in its RFM visualizations, ensuring revenue and customer count reconciliation.

- **ADR-018: Strict Separation of Presentation and Processing**
  - **Context**: Streamlit makes it easy to write data processing logic inside the frontend view file.
  - **Decision**: Restricted `app.py` exclusively to importing `load_all_analytics()` from `src.analytics.analytics`, UI layout definitions, and `plotly.express` rendering logic. No pandas data aggregation or calculation occurs within the Streamlit file except layout extraction.
  - **Consequences**: Ensures robust performance, allows isolated unit testing of the data layer without involving Streamlit, and maintains architectural integrity.

### Phase 7

- **ADR-019: Public Deployment Blocker Acceptance**
  - **Context**: The Phase 7 implementation plan requires provisioning a hosted PostgreSQL database (e.g., Supabase, Neon) and deploying a public Streamlit application via Streamlit Community Cloud.
  - **Decision**: Formally recorded the deployment task as BLOCKED. The execution environment lacks the necessary authenticated contexts (cloud provider API keys, GitHub OAuth sessions) to legitimately provision the infrastructure and deploy the application.
  - **Consequences**: Avoided fabricating deployment credentials or URLs. Preserved the integrity of the project state by accurately documenting the blocker while finalizing all local documentation and security audits.

## ADR-003
Decision: Target ~250,000 transactions in synthetic dataset
Reason: Large enough to make SQL analytics meaningful and demonstrate performance optimization, small enough to remain manageable on free-tier infrastructure
Alternatives considered: 50K (too small for performance demos), 1M+ (too large for free tier)
Why rejected: 50K insufficient for EXPLAIN ANALYZE demonstration; 1M+ risks storage/memory issues on free deployment
Affected resources: resources/IMPLEMENTATION_PLAN.md

## ADR-004
Decision: Use fixed random seed (SEED = 42)
Reason: Critical for reproducibility of synthetic dataset and analytical results
Alternatives considered: No seed (random each run)
Why rejected: Non-reproducible data makes debugging and validation impossible
Affected resources: resources/IMPLEMENTATION_PLAN.md, resources/prompts/PHASE_01_DATA.md

## ADR-005
Decision: Deploy on Streamlit Cloud with cloud PostgreSQL (Neon/Supabase/Railway)
Reason: Free tier available, minimal configuration, native Streamlit support
Alternatives considered: Heroku, Render, self-hosted
Why rejected: Streamlit Cloud offers simplest deployment path with free tier; others require more configuration
Affected resources: resources/IMPLEMENTATION_PLAN.md, resources/prompts/PHASE_06_DEPLOYMENT.md

## ADR-006
Decision: Use star-schema-inspired structure (customers → transactions ← products)
Reason: Simplest schema that supports all required analytics (RFM, cohort, category analysis)
Alternatives considered: Full dimensional model, snowflake schema
Why rejected: Unnecessary complexity for the analytical requirements
Affected resources: resources/IMPLEMENTATION_PLAN.md, resources/prompts/PHASE_02_DATABASE.md

## ADR-008
Decision: Provision portable user-space PostgreSQL binary
Reason: Bypasses the lack of administrator privileges for a system-level install, while fulfilling the strict requirement for a real PostgreSQL server.
Alternatives considered: SQLite, Chocolatey Postgres (system service)
Why rejected: SQLite explicitly prohibited. Chocolatey install failed due to no admin rights.
Affected resources: project_state/phases/phase_02_database.md
