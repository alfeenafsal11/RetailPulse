# Phase 02 — Database

Status: NOT_STARTED

Objective: Create PostgreSQL schema, load synthetic data from CSV, verify counts.

Resource prompt: resources/prompts/PHASE_02_DATABASE.md

Implementation-plan requirements:
- database/schema.sql with PKs, FKs
- database/seed.py for CSV loading
- src/config.py for DB configuration
- src/db.py for connection utilities
- .env.example for credentials documentation
- Row count verification

Inputs:
- data/raw/customers.csv
- data/raw/products.csv
- data/raw/transactions.csv

Outputs:
- database/schema.sql
- database/seed.py
- src/config.py
- src/db.py
- .env.example
- Populated PostgreSQL database

Implementation: Not started

Validation: Not started

Plan compliance: Not started

Problems: None

Decisions: None yet

Metrics: None yet

Known limitations: None yet

Next phase: PHASE_03_ANALYTICS

Resume instructions: Read STATE.md, then this file, then the phase prompt.
