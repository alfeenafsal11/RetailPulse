# PHASE 02 — PostgreSQL Schema and Data Loading

## Objective

Create the PostgreSQL database schema, load the synthetic dataset from CSV files, and verify data integrity in the database.

## Scope

- SQL schema with proper PKs and FKs
- Python data loading script
- Database connection configuration
- Row count verification

## Inputs

- CSV files from Phase 1: `data/raw/customers.csv`, `data/raw/products.csv`, `data/raw/transactions.csv`
- `resources/IMPLEMENTATION_PLAN.md` — database schema section

## Required Implementation Tasks

1. Create `database/schema.sql`:
   - CREATE TABLE customers with appropriate types and PK
   - CREATE TABLE products with appropriate types and PK
   - CREATE TABLE transactions with appropriate types, PK, and FKs
   - Use appropriate data types (TIMESTAMP, NUMERIC, VARCHAR, etc.)
   - Include DROP TABLE IF EXISTS for idempotency

2. Create `database/seed.py`:
   - Read database connection from environment variables
   - Execute schema.sql to create tables
   - Load CSV files into PostgreSQL using COPY or batch INSERT
   - Verify row counts match CSV files
   - Report load times

3. Create `src/config.py`:
   - Database connection configuration from environment
   - Default values for local development

4. Create `src/db.py`:
   - Database connection utility functions
   - Connection string builder

5. Create `.env.example`:
   - Document required environment variables
   - DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

6. Execute the loading pipeline and verify

## Required Files

```
database/schema.sql
database/seed.py
src/config.py
src/db.py
.env.example
```

## Validation Checks

- [ ] schema.sql executes without errors
- [ ] Tables created with correct columns and types
- [ ] Primary keys enforced
- [ ] Foreign keys enforced
- [ ] seed.py loads all three CSVs
- [ ] Customer count in DB matches CSV
- [ ] Product count in DB matches CSV
- [ ] Transaction count in DB matches CSV
- [ ] Sample queries return expected data
- [ ] No secrets in committed files

## Expected Outputs

- PostgreSQL database with three tables populated
- Schema file for reproducibility
- Loading script
- Configuration utilities

## Definition of Done

PostgreSQL database is populated with the complete dataset. Row counts verified. Schema is reproducible. Connection configuration is documented.

## Handoff Requirements

- Database is populated and queryable
- Row counts recorded in METRICS.md
- Load time recorded in METRICS.md
- Connection configuration documented in .env.example
- STATE.md updated

## STOP INSTRUCTION

**Do NOT execute PHASE 3 after completing PHASE 2.**

Stop after producing the Phase 2 completion report. Wait for explicit user instruction to proceed.
