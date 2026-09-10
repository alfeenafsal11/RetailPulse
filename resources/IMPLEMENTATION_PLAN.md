# RetailPulse — Implementation Plan

## Project Objective

Build a live, technically defensible retail customer analytics application demonstrating:
- Strong analytical SQL with PostgreSQL
- RFM segmentation and cohort retention analysis
- Query-performance diagnosis and optimization using EXPLAIN ANALYZE
- A functional Streamlit web application with public deployment
- Clear business interpretation and reproducible implementation

Target role: AI-Native Data Analyst Intern at Xeno.

## Target Architecture

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

## Technology Choices

| Component       | Technology            | Rationale                          |
|-----------------|-----------------------|------------------------------------|
| Language        | Python 3.11+          | Standard for data analytics        |
| Data            | NumPy, Pandas         | Data generation and manipulation   |
| Database        | PostgreSQL            | Strong SQL, relevant for target role |
| DB Driver       | psycopg2-binary       | Standard PostgreSQL adapter        |
| ORM/Engine      | SQLAlchemy            | Connection management              |
| Web App         | Streamlit             | Fastest route to live analytics app |
| Charts          | Plotly                | Interactive visualizations         |
| Config          | python-dotenv         | Environment variable management    |
| Deployment      | Streamlit Cloud       | Free, simple deployment            |
| Version Control | Git                   | Standard                           |

### Prohibited Technologies

Spark, Kafka, Airflow, dbt, Kubernetes, React, FastAPI, Redis, LangChain, LangGraph, LLM APIs, authentication, microservices, unnecessary cloud infrastructure.

---

## Dataset Design

### Entities

**Customers** (~10,000 rows)
- customer_id (PK)
- signup_date
- city
- age_group
- gender
- acquisition_channel
- customer_segment_ground_truth

**Products** (~500 rows)
- product_id (PK)
- category
- subcategory
- price
- cost

Product categories: Electronics, Fashion, Beauty, Home, Sports, Grocery, Accessories

**Transactions** (~250,000 rows)
- transaction_id (PK)
- customer_id (FK → customers)
- transaction_timestamp
- product_id (FK → products)
- quantity
- unit_price
- discount
- amount
- payment_method
- channel

### Behavioral Archetypes

The data generator must create customers with latent behavioral parameters that produce realistic RFM distributions:

| Archetype     | Frequency | Monetary  | Recency      |
|---------------|-----------|-----------|--------------|
| Champions     | High      | High      | Recent       |
| Loyal         | Med/High  | Consistent| Regular      |
| New           | Low       | Varies    | Very Recent  |
| At Risk       | Historical| Historical| Long gap     |
| Lost          | Historical| Historical| Very long gap|

Each customer is assigned:
- propensity_to_purchase
- average_order_value
- preferred_category
- purchase_frequency
- inactivity_probability

Transactions are sampled from these latent characteristics.

### Data Generation Algorithm

1. Set seed (SEED = 42)
2. Generate customers with demographic attributes
3. Assign behavioral parameters per archetype
4. Generate products across categories
5. Generate transaction timestamps per customer behavior
6. Generate purchases (quantity, price, discount) per behavior
7. Calculate amount = quantity × unit_price − discount
8. Validate all constraints
9. Save to CSV

### Data Validation Requirements

Before PostgreSQL load, validate:
- customer_id uniqueness
- product_id uniqueness
- transaction_id uniqueness
- Foreign key integrity (all customer_ids and product_ids exist)
- NULL rates acceptable
- No negative amounts
- No invalid timestamps
- No duplicate transactions
- Amount consistency: quantity × unit_price − discount ≈ amount
- Generator must fail loudly on validation failure

---

## Database Schema

Star-schema-inspired structure:

```
customers (1) ──── (N) transactions (N) ──── (1) products
```

### Files

- `database/schema.sql` — CREATE TABLE statements with PKs and FKs
- `database/indexes.sql` — Performance indexes (applied in Phase 4)
- `database/seed.py` — CSV loading script with count verification

### Loading Pipeline

1. Generate data → CSV
2. Create database
3. Create tables (schema.sql)
4. Load CSV data (seed.py)
5. Verify row counts

---

## Analytical SQL Requirements

### KPI Queries (`sql/kpi_queries.sql`)

| KPI                  | Definition                                      |
|----------------------|-------------------------------------------------|
| Total Revenue        | SUM(amount)                                     |
| Active Customers     | COUNT(DISTINCT customer_id) in analysis period  |
| Average Order Value  | total_revenue / transaction_count               |
| Repeat Purchase Rate | customers_with_≥2_purchases / customers_with_≥1 |

### RFM Segmentation (`sql/rfm.sql`)

For every customer, calculate:
- **Recency**: analysis_date − last_purchase_date
- **Frequency**: COUNT(transactions)
- **Monetary**: SUM(amount)

Score each dimension 1–5 using NTILE(5).

Segment mapping:

| Segment              | R Score | F Score | M Score |
|----------------------|---------|---------|---------|
| Champions            | 4–5     | 4–5     | 4–5     |
| Loyal Customers      | 3–5     | 3–5     | 3–5     |
| Potential Loyalists   | 3–5     | 1–3     | 1–3     |
| At Risk              | 1–2     | 3–5     | 3–5     |
| Lost                 | 1–2     | 1–2     | 1–2     |
| New Customers        | 4–5     | 1–1     | 1–1     |

Segmentation rules must be documented in the SQL file.

### Cohort Retention (`sql/retention.sql`)

Calculate:
- Signup/acquisition month per customer
- Purchase activity in subsequent months
- Output: cohort_month, months_since_acquisition, customers, retention_rate

### Customer/Category Analysis (`sql/customer_analysis.sql`)

- Revenue by category
- Transactions by category
- AOV by category
- Customers by category
- Revenue concentration: Top 1%, 5%, 10%, 20% customer contribution

---

## RFM Methodology

1. Set analysis reference date (MAX(transaction_timestamp) + 1 day)
2. Calculate raw R, F, M values per customer
3. Score using NTILE(5) window function
4. Map (R, F, M) scores to segments using documented rules
5. Validate: every customer assigned exactly one segment
6. Compare computed segments against ground-truth labels for reasonableness

---

## Cohort Methodology

1. Determine each customer's cohort (month of first purchase or signup)
2. For each subsequent month, check if customer made a purchase
3. Calculate retention_rate = active_customers_in_month / cohort_size
4. Output pivot-style cohort × months_since_acquisition matrix
5. Validate: Month 0 retention should be ~100%

---

## Performance-Analysis Methodology

### Files
- `sql/performance/before.sql` — Deliberately inefficient query
- `sql/performance/after.sql` — Optimized query

### Approach
1. Write a query with a known inefficiency (e.g., function on indexed column in WHERE clause)
2. Run EXPLAIN ANALYZE, record: execution time, planning time, scan method, rows scanned
3. Apply optimization (index creation, predicate rewrite, reduced SELECT *)
4. Run EXPLAIN ANALYZE again
5. Record before/after comparison

### Optimization Techniques (as applicable)
- Functional predicate rewrite
- B-tree index on filter columns
- Composite index
- Partitioning discussion (not necessarily implemented)
- Reduced SELECT *

### Required Output

| Metric          | Before    | After     |
|-----------------|-----------|-----------|
| Execution time  | measured  | measured  |
| Planning time   | measured  | measured  |
| Scan type       | measured  | measured  |
| Rows processed  | measured  | measured  |

All values must be actually measured, never fabricated.

---

## Streamlit Application Requirements

### Page Structure

```
RetailPulse
Customer Retention & Revenue Intelligence

[Total Revenue] [Customers] [Repeat Rate] [AOV]

Revenue Trend
────────────────────────

Customer Segments (RFM)
────────────────────────

Retention Cohorts
────────────────────────

Revenue by Category
────────────────────────

Top Customers
────────────────────────
```

### Features
- KPI metric cards at top
- Revenue trend chart (time series)
- RFM segment distribution (bar/pie chart)
- Cohort retention heatmap
- Category revenue breakdown
- Top customers table
- Date filter (if time permits)
- Category filter (if time permits)
- Segment filter (if time permits)

### Caching
- Use `@st.cache_data` for analytical query results
- Use `@st.cache_resource` for database connections

### Files
- `app/streamlit_app.py` — Main application
- `src/config.py` — Configuration management
- `src/db.py` — Database connection utilities
- `src/analytics.py` — Python analytics layer calling SQL

---

## Deployment Requirements

- Platform: Streamlit Cloud (free tier)
- Database: Cloud PostgreSQL (e.g., Neon, Supabase, or Railway free tier)
- Requirements: `requirements.txt` must be deployment-ready
- Secrets: Use Streamlit secrets management, no secrets in git
- Verification: Application must be accessible from a public URL
- `.env.example` must document required environment variables

---

## Validation Requirements

### Per-Phase Validation
Each phase has specific validation checks defined in its phase prompt.

### Final Validation (Phase 7)
- [ ] Repository works from clean setup
- [ ] Dataset generation is reproducible (seed=42)
- [ ] Data validation passes
- [ ] PostgreSQL schema created
- [ ] Data successfully loaded
- [ ] SQL KPI queries work
- [ ] RFM segmentation works
- [ ] Cohort retention works
- [ ] Performance experiment exists with real measurements
- [ ] EXPLAIN ANALYZE evidence recorded
- [ ] Streamlit application works
- [ ] Application is publicly accessible
- [ ] README explains architecture and business insights
- [ ] Git history is clean
- [ ] No secrets committed
- [ ] STATE.md is current
- [ ] EVENTS.md is current

---

## Phase Dependencies

```
PHASE 0: Bootstrap
    │
    ▼
PHASE 1: Data Generation
    │
    ▼
PHASE 2: PostgreSQL Schema & Loading
    │
    ▼
PHASE 3: Analytical SQL
    │
    ▼
PHASE 4: Query Performance
    │
    ▼
PHASE 5: Streamlit Application
    │
    ▼
PHASE 6: Public Deployment
    │
    ▼
PHASE 7: Final Validation & Documentation
```

Phases are strictly sequential. Do not parallelize.

---

## Phase Definitions of Done

### PHASE 0 — Bootstrap
- Repository structure exists
- All resource files created and coherent
- All state files created
- Git initialized
- No application code created

### PHASE 1 — Data Generation
- `src/data_generator.py` exists and runs
- Generates ~10K customers, ~500 products, ~250K transactions
- CSV files saved to `data/raw/`
- Data validation passes all checks
- Seed=42 produces identical output on re-run

### PHASE 2 — Database
- `database/schema.sql` creates tables with PKs and FKs
- `database/seed.py` loads CSVs into PostgreSQL
- Row counts verified from database
- `.env.example` documents connection variables

### PHASE 3 — Analytics
- All four SQL files exist and execute correctly
- KPIs return valid values
- RFM assigns every customer a segment
- Cohort retention matrix is valid
- Revenue concentration calculated
- `src/analytics.py` wraps SQL queries in Python

### PHASE 4 — Performance
- `sql/performance/before.sql` contains inefficient query
- `sql/performance/after.sql` contains optimized query
- EXPLAIN ANALYZE output recorded
- Before/after comparison table in METRICS.md
- Real measured values, not fabricated

### PHASE 5 — Streamlit App
- `app/streamlit_app.py` runs locally
- Displays all required sections
- Connects to PostgreSQL
- Uses caching

### PHASE 6 — Deployment
- Application publicly accessible
- URL recorded in README and STATE.md
- Database accessible from deployment

### PHASE 7 — Final Validation
- All validation checks pass
- README complete with architecture, insights, demo link
- Documentation current
- Git history clean

---

## Known Limitations

- Synthetic data will not perfectly match real retail distributions
- Free-tier cloud databases have performance/storage limits
- Streamlit Cloud free tier may have cold-start latency
- Query performance results depend on local PostgreSQL configuration
- No real-time data pipeline (batch analytics only)

## Time-Saving Constraints

- Use simple star schema, not full dimensional model
- No automated CI/CD pipeline
- No automated testing framework (manual validation sufficient)
- Dashboard is functional, not visually polished
- Single-page Streamlit layout
- No authentication or multi-tenancy
- Campaign interactions table is optional (Phase 2 only if time permits)
