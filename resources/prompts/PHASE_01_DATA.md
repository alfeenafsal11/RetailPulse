# PHASE 01 — Synthetic Data Generation

## Objective

Generate a realistic synthetic retail transaction dataset with behavioral customer archetypes that will produce meaningful RFM segmentation and cohort retention results.

## Scope

- Implement data generator in Python
- Generate customers, products, and transactions with realistic behavioral patterns
- Validate data integrity
- Save to CSV

## Inputs

- Repository structure from Phase 0
- `resources/IMPLEMENTATION_PLAN.md` — dataset design section
- No external data sources required

## Required Implementation Tasks

1. Create `src/data_generator.py` with:
   - Fixed random seed (SEED = 42)
   - Customer generation (~10,000) with demographic attributes
   - Customer behavioral archetype assignment (Champions, Loyal, New, At Risk, Lost)
   - Latent behavioral parameters per customer (propensity, AOV, frequency, preferred category, inactivity)
   - Product generation (~500) across 7 categories with price/cost
   - Transaction generation (~250,000) driven by customer behavioral parameters
   - Amount calculation: quantity × unit_price − discount = amount
   - Data validation built into the generator

2. Create `tests/test_data.py` with validation checks:
   - ID uniqueness (customer, product, transaction)
   - Foreign key integrity
   - No NULL in required fields
   - No negative amounts
   - Timestamp validity
   - Amount consistency
   - Row count verification
   - Distribution reasonableness

3. Run the generator and save outputs:
   - `data/raw/customers.csv`
   - `data/raw/products.csv`
   - `data/raw/transactions.csv`

4. Verify reproducibility: running with same seed produces identical output

## Required Files

```
src/data_generator.py
tests/test_data.py
data/raw/customers.csv
data/raw/products.csv
data/raw/transactions.csv
```

## Validation Checks

- [ ] Generator runs without errors
- [ ] customers.csv has ~10,000 rows
- [ ] products.csv has ~500 rows
- [ ] transactions.csv has ~250,000 rows
- [ ] All customer_ids in transactions exist in customers
- [ ] All product_ids in transactions exist in products
- [ ] No duplicate IDs
- [ ] No negative amounts
- [ ] Amount ≈ quantity × unit_price − discount
- [ ] Timestamps are within expected range
- [ ] Multiple customer segments are represented
- [ ] Re-running with seed=42 produces identical CSVs

## Expected Outputs

- Three CSV files in `data/raw/`
- Validated, reproducible synthetic dataset
- Data generator script
- Validation test script

## Definition of Done

Data generator produces validated CSVs with realistic behavioral distributions. All validation checks pass. Dataset is reproducible with seed=42.

## Handoff Requirements

- CSVs ready for PostgreSQL loading in Phase 2
- Row counts recorded in METRICS.md
- Data validation results recorded
- STATE.md updated with Phase 1 completion

## STOP INSTRUCTION

**Do NOT execute PHASE 2 after completing PHASE 1.**

Stop after producing the Phase 1 completion report. Wait for explicit user instruction to proceed.
