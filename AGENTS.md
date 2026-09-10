# Agent Operating Rules

## Context Recovery

1. Read `project_state/STATE.md` before making changes.
2. Read `project_state/DECISIONS.md` before changing architecture.
3. Read `resources/IMPLEMENTATION_PLAN.md` before implementing any phase.
4. Read the current phase prompt from `resources/prompts/` before implementation.
5. Read the current phase file from `project_state/phases/` before implementation.

## Implementation Rules

6. Follow the implementation plan fully.
7. Do not redesign completed phases without evidence of failure.
8. Work only on the current phase unless explicitly instructed otherwise.
9. Prefer modifying existing implementation over creating parallel implementations.
10. Do not add dependencies unless necessary.
11. Do not introduce infrastructure not required by the project objective.
12. Prefer the simplest implementation that satisfies the plan.
13. Do not optimize prematurely.
14. Do not spend time polishing UI before core functionality works.
15. Do not implement speculative functionality.

## Verification Rules

16. Run relevant verification after every meaningful change.
17. Validate both implementation correctness and plan compliance.
18. Never fabricate test results, benchmark results, dataset sizes, or deployment status.
19. Never claim a feature is implemented unless it actually works.
20. Never claim a planned requirement is complete unless it has been checked.

## State Management

21. Record important events in `project_state/EVENTS.md`.
22. Update `STATE.md` when phase status changes.
23. Record architectural changes in `DECISIONS.md`.
24. Record measured values in `METRICS.md`.
25. Keep state files concise.

## Error Handling

26. If blocked, diagnose and document the blocker before attempting broad redesign.
27. Preserve working functionality while adding new functionality.
28. Record important failures in `EVENTS.md` and the current phase file.
29. Do not silently skip a requirement from the implementation plan.
30. Do not begin the next phase merely because the current phase finished early.

## Resource Hierarchy

When instructions conflict, follow this precedence:

1. Current user instruction
2. `resources/IMPLEMENTATION_PLAN.md`
3. Current phase prompt in `resources/prompts/`
4. This file (`AGENTS.md`)
5. `project_state/STATE.md`
6. Current phase file
7. Other project documentation

If two project files conflict, record the conflict and resolution in `project_state/DECISIONS.md`.

## Prohibited Technologies

Do NOT introduce without explicit instruction:
- Spark, Kafka, Airflow, dbt
- Kubernetes, React, FastAPI, Redis
- LangChain, LangGraph, LLM APIs
- Authentication, microservices
- Unnecessary cloud infrastructure
