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
