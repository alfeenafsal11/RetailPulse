# PHASE 04 — Query Performance Investigation and Optimization

## Objective

Demonstrate query-performance diagnosis and optimization methodology using EXPLAIN ANALYZE. Create a before/after comparison with real measured performance data.

## Scope

- Create deliberately inefficient query
- Measure baseline performance
- Apply optimization
- Measure optimized performance
- Record real metrics
- Create performance indexes

## Inputs

- Populated PostgreSQL database from Phase 2
- Working SQL queries from Phase 3
- `resources/IMPLEMENTATION_PLAN.md` — performance-analysis methodology section

## Required Implementation Tasks

1. Create `sql/performance/before.sql`:
   - Write a query with a known inefficiency
   - Example: date filter using EXTRACT() or TO_CHAR() on timestamp column (prevents index usage)
   - Include EXPLAIN ANALYZE output capture
   - Query must be analytically relevant (not contrived)

2. Create `sql/performance/after.sql`:
   - Rewrite the query with optimization applied
   - Apply one or more techniques:
     - Functional predicate rewrite (e.g., range comparison instead of function)
     - Index creation (B-tree on relevant columns)
     - Composite index where beneficial
     - Reduced SELECT * to specific columns
   - Include EXPLAIN ANALYZE output capture

3. Create `database/indexes.sql`:
   - Performance indexes identified during optimization
   - Indexes for common analytical query patterns
   - Document rationale for each index

4. Run the performance experiment:
   - Execute before.sql with EXPLAIN ANALYZE
   - Record: execution time, planning time, scan method, rows scanned
   - Apply optimization (create indexes, rewrite query)
   - Execute after.sql with EXPLAIN ANALYZE
   - Record: execution time, planning time, scan method, rows scanned

5. Record results in METRICS.md:
   - Before/after comparison table
   - All values must be actually measured
   - Include improvement percentage

## Required Files

```
sql/performance/before.sql
sql/performance/after.sql
database/indexes.sql
```

## Validation Checks

- [ ] before.sql executes without errors
- [ ] after.sql executes without errors
- [ ] EXPLAIN ANALYZE output captured for both queries
- [ ] Before performance metrics recorded (execution time, scan type, rows)
- [ ] After performance metrics recorded
- [ ] Performance improvement demonstrated
- [ ] All metrics are real measurements, not fabricated
- [ ] Optimization technique is documented
- [ ] indexes.sql executes without errors
- [ ] Results recorded in METRICS.md

## Expected Outputs

- Before/after SQL files with EXPLAIN ANALYZE evidence
- Index creation script
- Measured performance comparison in METRICS.md

## Definition of Done

Before/after queries exist and execute. EXPLAIN ANALYZE output is captured and recorded. Performance improvement is demonstrated with real measurements. All metrics in METRICS.md are actual observations.

## Handoff Requirements

- Performance metrics recorded in METRICS.md
- Indexes applied to database
- Performance methodology ready for README documentation
- STATE.md updated

## STOP INSTRUCTION

**Do NOT execute PHASE 5 after completing PHASE 4.**

Stop after producing the Phase 4 completion report. Wait for explicit user instruction to proceed.
