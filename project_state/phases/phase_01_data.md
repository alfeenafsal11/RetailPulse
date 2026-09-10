# Phase 01 — Data Generation

Status: NOT_STARTED

Objective: Generate reproducible synthetic retail transaction dataset with behavioral customer archetypes.

Resource prompt: resources/prompts/PHASE_01_DATA.md

Implementation-plan requirements:
- data_generator.py with seed=42
- ~10K customers with behavioral archetypes
- ~500 products across 7 categories
- ~250K transactions driven by customer behavior
- Data validation (IDs, FKs, amounts, timestamps)
- CSV output to data/raw/

Inputs: None (generates from scratch)

Outputs:
- src/data_generator.py
- tests/test_data.py
- data/raw/customers.csv
- data/raw/products.csv
- data/raw/transactions.csv

Implementation: Not started

Validation: Not started

Plan compliance: Not started

Problems: None

Decisions: None yet

Metrics: None yet

Known limitations: None yet

Next phase: PHASE_02_DATABASE

Resume instructions: Read STATE.md, then this file, then the phase prompt.
