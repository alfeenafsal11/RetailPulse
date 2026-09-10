# RetailPulse — Customer Retention & Revenue Intelligence

A retail customer analytics application demonstrating SQL proficiency, RFM segmentation, cohort retention analysis, and query-performance optimization with PostgreSQL.

## Project Objective

Build a technically defensible retail analytics pipeline that:
- Generates realistic synthetic retail transaction data
- Loads it into PostgreSQL with a proper schema
- Performs analytical SQL (KPIs, RFM segmentation, cohort retention, revenue concentration)
- Investigates and optimizes query performance using `EXPLAIN ANALYZE`
- Presents results through a live Streamlit dashboard
- Deploys publicly

## Architecture

```
Synthetic Data Generator
        │
        ▼
  CSV Raw Dataset
        │
        ▼
 PostgreSQL Database
        │
   ┌────┼────────────┐
   ▼    ▼            ▼
 SQL  Performance  Data Quality
Analytics Experiments
   └────┼────────────┘
        ▼
 Python Analytics Layer
        │
        ▼
 Streamlit Web App
        │
        ▼
  LIVE DEPLOYMENT
```

## Tech Stack

| Component       | Technology         |
|-----------------|--------------------|
| Language        | Python 3.11+       |
| Database        | PostgreSQL         |
| Analytics       | SQL, Pandas, NumPy |
| Visualization   | Streamlit, Plotly  |
| Deployment      | Streamlit Cloud    |

## Dataset

- **Customers**: ~10,000 with behavioral archetypes
- **Products**: ~500 across 7 categories
- **Transactions**: ~250,000 with realistic purchase patterns

## Analytics

- **KPIs**: Total revenue, active customers, AOV, repeat purchase rate
- **RFM Segmentation**: Recency–Frequency–Monetary scoring with customer segments
- **Cohort Retention**: Monthly acquisition cohorts with retention rates
- **Revenue Concentration**: Top 1%/5%/10%/20% customer contribution
- **Category Analysis**: Revenue, transactions, AOV by product category

## Query Performance

Demonstrates query optimization methodology:
1. Write baseline query
2. Run `EXPLAIN ANALYZE`
3. Identify bottleneck
4. Apply optimization (index, predicate rewrite, etc.)
5. Re-run `EXPLAIN ANALYZE`
6. Compare metrics

## Project Status

**Current Phase**: PHASE 0 — Bootstrap  
See [project_state/STATE.md](project_state/STATE.md) for live status.

## Setup

```bash
# Clone
git clone <repo-url>
cd retailpulse

# Install dependencies
pip install -r requirements.txt

# Generate data
python src/data_generator.py

# Initialize database
psql -f database/schema.sql
python database/seed.py

# Run application
streamlit run app/streamlit_app.py
```

## Live Demo

*Deployment URL will be added in Phase 6.*

## License

MIT
