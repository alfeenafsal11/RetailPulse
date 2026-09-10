# RetailPulse — Customer Retention & Revenue Intelligence

A data analytics engineering project demonstrating SQL proficiency, PostgreSQL optimization, and full-stack analytics implementation.

This project processes **synthetic retail data** to demonstrate the analytics engineering workflow. It is not real business data.

## Project Positioning

RetailPulse explicitly demonstrates:
- **SQL Analytics**: Multi-join aggregations, window functions, and CTEs.
- **PostgreSQL**: Robust schema design, primary/foreign keys, and strict typing.
- **Query Optimization**: Using `EXPLAIN ANALYZE`, indexing, and join reordering.
- **Business Logic**: RFM customer segmentation, cohort retention heatmaps, and revenue concentration.
- **Data Engineering**: Deterministic synthetic data generation (245,210 transactions).
- **Python/Pandas**: Type enforcement, invariant validation, and presentation formatting.
- **Streamlit**: Hosted, database-backed interactive analytics dashboard.

## Architecture

The project strictly separates aggregation, validation, and presentation:

```
Synthetic retail data (data_generator.py)
        ↓
PostgreSQL star schema (database/schema.sql)
        ↓
Analytical SQL (sql/analytics/*.sql)
        ↓
Python/pandas data layer (src/analytics/analytics.py)
        ↓
Streamlit dashboard (app/app.py)
```

### Responsibility Split
- **PostgreSQL**: Source of truth for massive aggregations, joins, RFM scoring, cohorts, and revenue analysis.
- **Python**: Loads SQL results, enforces precise typing, runs automated validation (`unittest`), and executes dashboard-ready transformations (e.g., pivoting cohorts).
- **Streamlit**: Dedicated entirely to presentation, interaction, and data visualization. No raw aggregations happen here.

## Dataset

- **Customers**: 10,000 (synthetic behavioral archetypes)
- **Products**: 500 across 7 categories
- **Transactions**: 245,210 transactions
- **Total Revenue**: $53,581,128.12
- **Date Range**: 2024-07-01 to 2026-06-30

## Query Performance

Demonstrates a systematic optimization methodology using `EXPLAIN ANALYZE`:

**Local PostgreSQL Performance Experiment:**
- `customer_metrics.sql` baseline: ≈ 230 ms
- Optimization: Pre-aggregating transactions by customer in a CTE before joining to the customer dimension.
- `customer_metrics.sql` optimized: ≈ 139 ms
- Improvement: **≈39% reduction in execution time**.

*Note: An RFM index experiment was also performed, where it was proven that PostgreSQL's sequential scan remained preferable for the full-table aggregation workload.*

## Project Status

**Current Phase**: PHASE 7 — Deployment (BLOCKED)
See [project_state/STATE.md](project_state/STATE.md) for full state.

## Local Reproducibility Pipeline

1. **Prerequisite**: Python 3.11+ and PostgreSQL must be running locally.

```bash
# Clone
git clone <repo-url>
cd retailpulse

# Install dependencies
pip install -r requirements.txt

# Generate synthetic dataset (deterministic via SEED=42)
python src/data_generator.py

# Create schema and load database
psql -d postgres -f database/schema.sql
python database/seed.py

# Set up local environment variables (.env)
# POSTGRES_HOST=localhost
# POSTGRES_PORT=5432
# POSTGRES_DB=postgres
# POSTGRES_USER=<your-user>
# POSTGRES_PASSWORD=<your-password>

# Validate the pipeline
python tests/test_analytics.py
python tests/test_python_analytics.py

# Launch Streamlit locally
python -m streamlit run app/app.py
```

## Public Deployment

The application is architected for Streamlit Cloud deployment connected to a hosted PostgreSQL backend.
*(Deployment currently blocked by lack of accessible cloud PostgreSQL/Streamlit credentials in the development environment).*

## License

MIT
