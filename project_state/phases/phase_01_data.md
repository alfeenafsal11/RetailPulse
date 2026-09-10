# Phase 01 — Data Generation

Status: COMPLETE

Objective: Generate reproducible synthetic retail transaction dataset with behavioral customer archetypes.

Resource prompt: resources/prompts/PHASE_01_DATA.md

Implementation-plan requirements:
- [x] data_generator.py with seed=42
- [x] ~10K customers with behavioral archetypes (Champion, Loyal, New, At Risk, Lost)
- [x] ~500 products across 7 categories
- [x] ~250K transactions driven by customer behavior (actual: 245,210)
- [x] Data validation (IDs, FKs, amounts, timestamps)
- [x] CSV output to data/raw/
- [x] Reproducibility test (MD5 hash comparison)

Inputs: None (generates from scratch)

Outputs:
- src/data_generator.py
- tests/test_data.py
- tests/test_reproducibility.py
- data/raw/customers.csv (519 KB, 10,000 rows)
- data/raw/products.csv (17 KB, 500 rows)
- data/raw/transactions.csv (18.6 MB, 245,210 rows)

Implementation:
- 5 behavioral archetypes with latent parameters (frequency, AOV, preferred category, inactivity)
- Transactions generated per-customer based on archetype parameters
- Amount = quantity * unit_price - discount (exact)
- Date range: 2024-07-01 to 2026-06-30 (24 months)
- 7 product categories, 5 payment methods, 3 channels

Validation: PASS (50/50 checks)
- ID uniqueness: PASS
- Foreign key integrity: PASS
- Required fields (no NULLs): PASS
- Amount consistency: PASS (max diff = 0.0000)
- Timestamp validity: PASS
- Distribution sanity: PASS

Plan compliance: PASS

Actual metrics:
- Customers: 10,000
- Products: 500
- Transactions: 245,210
- Generation time: ~31s
- Validation time: ~0.2s
- CSV sizes: customers 519 KB, products 17 KB, transactions 18.6 MB
- Segment distribution: Champion 10%, Loyal 20%, New 20%, At Risk 25%, Lost 25%
- Transactions per segment: Loyal 74,876, At Risk 68,708, Champion 59,925, Lost 31,791, New 9,910

Reproducibility: PASS
- MD5 customers.csv: f0b018f65b63efddb7c7417f5b653ac6
- MD5 products.csv: 695ab66869a92ccdc0b1786d1fe9a351
- MD5 transactions.csv: 9171aa5a308b0dcfd8bed7cf42c69e22

Problems: None

Decisions:
- Increased purchase frequency ranges from initial implementation to reach ~250K target (first run produced 171K)
- CSVs excluded from git tracking (18 MB too large) — regenerable via `python src/data_generator.py`

Known limitations:
- Generation takes ~31s due to per-customer loop (acceptable for one-time generation)
- Transaction count (245,210) is 2% below target (within 30% tolerance)

Next phase: PHASE_02_DATABASE (resources/prompts/PHASE_02_DATABASE.md)

Resume instructions:
1. Read project_state/STATE.md
2. Read resources/IMPLEMENTATION_PLAN.md
3. Read resources/prompts/PHASE_02_DATABASE.md
4. Ensure data/raw/ CSVs exist (run `python src/data_generator.py` if not)
5. Create database/schema.sql, database/seed.py, src/config.py, src/db.py
