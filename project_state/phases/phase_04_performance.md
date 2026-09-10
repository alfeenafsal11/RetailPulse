# Phase 04 — PostgreSQL Query Performance & Index Optimization

Status: COMPLETE

Objective: Conduct an empirical PostgreSQL query-performance investigation using `EXPLAIN ANALYZE`, identify bottlenecks, test optimization hypotheses, and document findings based on actual execution metrics.

Resource prompt: resources/prompts/PHASE_04_PERFORMANCE.md

Implementation-plan requirements:
- [x] Select at least two meaningful workloads from Phase 3
- [x] Establish a clean execution baseline using `EXPLAIN ANALYZE`
- [x] Interpret execution plans (access paths, joins, aggregations)
- [x] Test index / query optimizations
- [x] Compare baseline vs optimized execution times
- [x] Ensure semantic correctness is preserved
- [x] Document findings in `sql/performance/benchmark_analysis.md`

Workloads Investigated:
1. `sql/analytics/customer_metrics.sql`
2. `sql/analytics/rfm.sql`

Key Findings:
1. **Pre-aggregation Optimization (`customer_metrics.sql`)**:
   - Baseline: ~230 ms. The query performed a Hash Right Join of all 245,210 transactions with the 10,000 customers table *before* aggregating, which resulted in a massive HashAggregate.
   - Optimization: Rewrote the query to aggregate `transactions` in a CTE before joining to `customers`. 
   - Result: Execution time dropped to ~139 ms. The join cardinality dropped from 245,210 to 10,000, allowing for a much faster Hash Left Join.
2. **Index Rejection Analysis (`rfm.sql`)**:
   - Baseline: ~168 ms. PostgreSQL chose a Sequential Scan despite the existence of `idx_transactions_customer`.
   - Experiment: Disabled sequential scans (`SET enable_seqscan = off`) to force the index scan.
   - Result: Execution time increased to ~197 ms. 
   - Conclusion: PostgreSQL correctly chose the Sequential Scan because calculating RFM requires aggregating the *entire* table without filtering. A sequential scan reading contiguous blocks is more I/O efficient than traversing a B-Tree index for 245k random heap fetches.

Outputs:
- `sql/performance/benchmark_analysis.md`
- `tests/benchmark.py`
- `tests/optimize_customer_metrics.py`
- `tests/test_rfm_index.py`

Validation: PASS
- Verified that all queries output the exact same analytical results (Revenue: $53,581,128.12).

Next phase: PHASE_05_PYTHON_ANALYTICS (resources/prompts/PHASE_05_ANALYTICS.md)

Resume instructions:
1. Read `project_state/STATE.md` and `resources/IMPLEMENTATION_PLAN.md`.
2. Follow instructions in `resources/prompts/PHASE_05_ANALYTICS.md`.
