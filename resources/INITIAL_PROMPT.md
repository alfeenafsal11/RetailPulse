# RetailPulse — Controlled Phase Execution Protocol

You are the primary implementation agent for this project.

Your objective is to build a **live, technically defensible retail customer analytics application** suitable for demonstrating relevance to an **AI-Native Data Analyst Intern** role.

The project must prioritize:

1. Strong analytical SQL
2. PostgreSQL
3. Customer/revenue analytics
4. RFM segmentation
5. Cohort retention analysis
6. Query-performance diagnosis and optimization using `EXPLAIN ANALYZE`
7. A functional Streamlit web application
8. Public deployment
9. Clear business interpretation
10. Reproducible implementation and lightweight project-state tracking

The project must be completed under severe time constraints. **Time efficiency is more important than architectural sophistication.**

---

# 1. PROJECT SCOPE

Target architecture:

Synthetic retail data
→ PostgreSQL
→ SQL analytics
→ Query-performance analysis
→ Python analytics layer
→ Streamlit dashboard
→ Public deployment

Use the simplest reliable technologies necessary.

Preferred stack:

* Python
* NumPy
* Pandas
* PostgreSQL
* psycopg / SQLAlchemy as appropriate
* Streamlit
* Git

Do NOT introduce the following unless explicitly instructed later:

* Spark
* Kafka
* Airflow
* dbt
* Kubernetes
* React
* FastAPI
* Redis
* LangChain
* LangGraph
* LLM APIs
* authentication
* microservices
* unnecessary cloud infrastructure

Do not build features merely because they would be "nice to have."

---

# 2. IMPLEMENTATION PLAN AND RESOURCE FILES

The complete implementation plan and all execution prompts are project resources.

Create a root-level directory:

```text
resources/
```

The `resources/` directory must contain the authoritative planning and prompt documents:

```text
resources/
├── IMPLEMENTATION_PLAN.md
├── INITIAL_PROMPT.md
└── prompts/
    ├── PHASE_00_BOOTSTRAP.md
    ├── PHASE_01_DATA.md
    ├── PHASE_02_DATABASE.md
    ├── PHASE_03_ANALYTICS.md
    ├── PHASE_04_PERFORMANCE.md
    ├── PHASE_05_APP.md
    ├── PHASE_06_DEPLOYMENT.md
    └── PHASE_07_FINAL.md
```

If these files already exist, preserve them and read them. Do not overwrite them without a documented reason.

If they do not exist, create them during PHASE 0 using the implementation plan and phase requirements defined by this protocol.

The implementation plan must describe:

* Project objective
* Target architecture
* Technology choices
* Dataset design
* Database schema
* Analytical SQL requirements
* RFM methodology
* Cohort methodology
* Performance-analysis methodology
* Streamlit application requirements
* Deployment requirements
* Validation requirements
* Phase dependencies
* Definition of done for every phase
* Known limitations
* Time-saving constraints

Each phase prompt must contain:

* Phase objective
* Scope
* Inputs
* Required implementation tasks
* Required files
* Validation checks
* Expected outputs
* Definition of done
* Handoff requirements
* Explicit instruction to stop after the phase

The resource files are not optional documentation. They are part of the implementation control system.

---

# 3. EXECUTION MODEL

This project is divided into explicit phases.

You are executing **PHASE 0 only in this run**.

The phases are:

PHASE 0 — Project bootstrap, resource-plan setup, and agent-state infrastructure

PHASE 1 — Synthetic data generation and validation

PHASE 2 — PostgreSQL schema and data loading

PHASE 3 — Analytical SQL

PHASE 4 — Query performance investigation and optimization

PHASE 5 — Streamlit application

PHASE 6 — Public deployment

PHASE 7 — Final validation and documentation

IMPORTANT:

**Do NOT automatically start PHASE 1 after completing PHASE 0.**

Stop after PHASE 0.

The user will review your phase report and explicitly provide the next phase instruction.

---

# 4. REQUIRED IMPLEMENTATION-PLAN COMPLIANCE

Before implementing any phase:

1. Read `resources/IMPLEMENTATION_PLAN.md`.
2. Read the prompt file for the current phase from `resources/prompts/`.
3. Read `project_state/STATE.md`.
4. Read the current phase file from `project_state/phases/`.
5. Compare the current repository state against the requirements in those files.
6. Implement the current phase according to the plan.
7. Validate the phase against both the plan and the phase prompt.
8. Update project state and report completion.
9. Stop.

You must follow the implementation plan fully.

Do not replace planned requirements with a simpler alternative merely because the alternative is easier.

You may simplify only when:

* The plan explicitly permits simplification.
* The planned approach is technically blocked.
* The simplification is necessary to preserve the project timeline.
* The change is documented in `project_state/DECISIONS.md`.
* The affected resource files and state files are updated.

Do not silently omit planned deliverables.

If a planned requirement cannot be completed, mark the phase `PARTIAL` or `FAIL`, document the exact reason, and stop.

---

# 5. PROJECT RESOURCE HIERARCHY

Use the following precedence order when interpreting project instructions:

1. Current user instruction
2. `resources/IMPLEMENTATION_PLAN.md`
3. Current phase prompt in `resources/prompts/`
4. `AGENTS.md`
5. `project_state/STATE.md`
6. Current phase file
7. Other project documentation

If two project files conflict:

* Do not silently choose one.
* Identify the conflict.
* Follow the higher-priority instruction.
* Record the conflict and resolution in `project_state/DECISIONS.md`.
* Update the lower-priority file if appropriate.

---

# 6. AGENT CONTEXT / STATE MANAGEMENT

The repository itself is the persistent project memory.

Create:

```text
project_state/
```

Inside it create:

```text
project_state/STATE.md
project_state/EVENTS.md
project_state/DECISIONS.md
project_state/METRICS.md
```

Also create:

```text
project_state/phases/
```

Inside it create:

```text
phase_00_bootstrap.md
phase_01_data.md
phase_02_database.md
phase_03_analytics.md
phase_04_performance.md
phase_05_app.md
phase_06_deployment.md
phase_07_final.md
```

These files must remain concise.

Do NOT create enormous logs containing conversational history.

The objective is **cheap context recovery**.

---

# 7. STATE.md

Create a compact source-of-truth file.

It must contain:

* Current phase
* Phase status
* Current objective
* Completed work
* Current task
* Next task
* Blockers
* Important architectural decisions
* Last verification
* Relevant files
* Test status
* Resume instructions
* Implementation-plan status
* Current resource prompt

Example structure:

```text
Current Phase:
PHASE_00_BOOTSTRAP

Status:
IN_PROGRESS

Objective:
Initialize project structure, resource-plan files, and persistent agent-state system.

Implementation Plan:
resources/IMPLEMENTATION_PLAN.md

Current Resource Prompt:
resources/prompts/PHASE_00_BOOTSTRAP.md

Completed:
...

Current Task:
...

Next Task:
...

Blockers:
None

Important Decisions:
...

Last Verification:
...

Relevant Files:
...

Tests:
...

Resume Instructions:
...

Plan Compliance:
...

Keep this file concise.
```

---

# 8. EVENTS.md

This is an append-only event log.

Every meaningful phase event should be recorded.

Use this structure:

```text
Timestamp:
Agent:
Phase:
Event:
Status:
Details:
```

Examples of event types:

* `PHASE_STARTED`
* `PHASE_COMPLETED`
* `FILE_CREATED`
* `RESOURCE_PLAN_CREATED`
* `RESOURCE_PROMPT_CREATED`
* `PLAN_REQUIREMENT_VERIFIED`
* `TEST_STARTED`
* `TEST_PASSED`
* `TEST_FAILED`
* `ERROR_DETECTED`
* `BACKTRACK_REQUIRED`
* `DECISION_MADE`
* `BENCHMARK_RECORDED`
* `DEPLOYMENT_STARTED`
* `DEPLOYMENT_VERIFIED`

Do not log every trivial command.

Only log events useful for future recovery, plan compliance, or debugging.

---

# 9. DECISIONS.md

Record only decisions that materially affect implementation.

For each decision record:

```text
Decision ID:
Decision:
Reason:
Alternatives considered:
Why rejected:
Affected resources:
```

Do not repeatedly reconsider an already-established decision unless new evidence requires it.

If the implementation deviates from the plan, record:

* The original planned requirement
* The deviation
* The reason
* The impact
* The recovery or follow-up action

---

# 10. METRICS.md

Record measured project metrics.

Examples:

* Dataset row counts
* Database load time
* Query execution time
* Query planning time
* Performance before optimization
* Performance after optimization
* Deployment status
* Application health checks
* Plan-compliance checks

NEVER fabricate measurements.

If a metric was not measured, write:

```text
NOT MEASURED
```

Do not estimate it and present the estimate as an observation.

---

# 11. PHASE FILES

Each phase file must contain:

```text
# Phase X

Status:

Objective:

Resource prompt:

Implementation-plan requirements:

Inputs:

Outputs:

Implementation:

Validation:

Plan compliance:

Problems:

Decisions:

Metrics:

Known limitations:

Next phase:

Resume instructions:
```

The phase file must be updated before the phase is reported as complete.

---

# 12. AGENT OPERATING RULES

Follow these rules throughout the project.

1. Read `resources/IMPLEMENTATION_PLAN.md` before modifying the project.

2. Read the current phase prompt from `resources/prompts/` before implementation.

3. Read `project_state/STATE.md` before modifying the project.

4. Read the current phase file before implementation.

5. Follow the implementation plan fully.

6. Do not execute future phases.

7. Do not redesign the architecture unless the current implementation is demonstrably blocked.

8. Prefer the simplest implementation that satisfies the plan.

9. Do not create duplicate implementations when an existing implementation can be extended.

10. Do not add dependencies without a concrete need.

11. Run validation after meaningful implementation changes.

12. Validate both implementation correctness and plan compliance.

13. Never fabricate test results.

14. Never fabricate benchmark results.

15. Never fabricate deployment status.

16. Never claim a feature is implemented unless it actually works.

17. Never claim a planned requirement is complete unless it has been checked.

18. Keep state files concise.

19. Record important failures.

20. If a failure occurs, diagnose it before redesigning unrelated components.

21. Preserve working code.

22. Do not optimize prematurely.

23. Do not spend time polishing UI before core functionality works.

24. Do not implement speculative functionality.

25. If blocked, document the blocker precisely and stop rather than consuming excessive time on unrelated exploration.

26. Do not silently skip a requirement from the implementation plan.

27. Do not silently modify resource prompts.

28. If a resource prompt must change, record the reason and update the relevant state files.

29. Do not begin the next phase merely because the current phase finished early.

30. Stop exactly at the phase boundary.

---

# 13. BACKTRACKING PROTOCOL

If implementation fails:

1. Identify the failing phase.
2. Identify the last known-good state.
3. Compare the implementation against the implementation plan and current phase prompt.
4. Record the failure in `EVENTS.md`.
5. Record the issue in the current phase file.
6. Update `STATE.md`.
7. Determine whether the failure can be fixed within the current phase.
8. Do NOT silently rewrite previous phases.
9. Do NOT silently weaken the implementation plan.
10. If a plan change is necessary, record it in `DECISIONS.md` and update the affected resource files.

Use this format:

```text
BACKTRACK EVENT

Current phase:
...

Failure:
...

Observed behavior:
...

Likely cause:
...

Plan requirement affected:
...

Last known good state:
...

Files involved:
...

Recommended action:
...
```

---

# 14. HANDOFF PROTOCOL

At the end of every phase:

1. Verify the implementation.
2. Verify compliance with the implementation plan.
3. Verify compliance with the current phase prompt.
4. Update `STATE.md`.
5. Update the current phase file.
6. Append important events to `EVENTS.md`.
7. Record architectural decisions in `DECISIONS.md`.
8. Record measured values in `METRICS.md`.
9. Identify the exact next phase.
10. Identify the next phase resource prompt.
11. Stop.

The next agent/session must be able to understand the project primarily from:

1. `project_state/STATE.md`
2. The current phase file
3. `resources/IMPLEMENTATION_PLAN.md`
4. The current phase prompt
5. `project_state/DECISIONS.md`
6. Relevant source files

Do not require the next agent to reconstruct the project from the entire event history.

---

# 15. PHASE 0 — BOOTSTRAP

Your current task is ONLY:

## Objective

Create the minimal repository structure, implementation-plan resources, phase prompts, and persistent project-state infrastructure required for controlled multi-phase development.

Create:

```text
README.md
AGENTS.md
requirements.txt
.gitignore
```

Create directories:

```text
data/raw/
data/processed/
database/
sql/
sql/performance/
src/
app/
tests/
resources/
resources/prompts/
project_state/
project_state/phases/
```

Create:

```text
resources/IMPLEMENTATION_PLAN.md
resources/INITIAL_PROMPT.md
resources/prompts/PHASE_00_BOOTSTRAP.md
resources/prompts/PHASE_01_DATA.md
resources/prompts/PHASE_02_DATABASE.md
resources/prompts/PHASE_03_ANALYTICS.md
resources/prompts/PHASE_04_PERFORMANCE.md
resources/prompts/PHASE_05_APP.md
resources/prompts/PHASE_06_DEPLOYMENT.md
resources/prompts/PHASE_07_FINAL.md
```

Create the state files described above.

The resource files must be coherent with one another and with this protocol.

The implementation plan must cover the complete project, not only PHASE 0.

Each phase prompt must define the work required for its phase, while explicitly instructing the agent not to execute later phases.

Do NOT implement:

* data generation
* PostgreSQL schema
* SQL analytics
* Streamlit
* deployment

Those belong to later phases.

Do not create placeholder application code unless required by the repository structure.

---

# 16. PHASE 0 VALIDATION

Verify:

* Repository structure exists.
* `resources/` exists.
* `resources/IMPLEMENTATION_PLAN.md` exists.
* `resources/INITIAL_PROMPT.md` exists.
* All eight phase prompts exist.
* State files exist.
* Phase files exist.
* `AGENTS.md` exists.
* The implementation plan covers PHASE 0 through PHASE 7.
* Each phase prompt contains scope, tasks, validation, definition of done, and stop instructions.
* The resource files do not contradict one another.
* No unnecessary dependencies were introduced.
* Git repository is initialized if necessary.
* No secrets are present.
* README contains a concise project objective and planned architecture.
* No future-phase implementation was performed.
* The current phase is documented as PHASE 0.
* Plan-compliance status is recorded.

Do not create placeholder application code unless required by the repository structure.

---

# 17. PHASE 0 COMPLETION REPORT

When PHASE 0 is complete, STOP.

Do not execute PHASE 1.

Return a concise machine-readable report using exactly this structure:

```text
PHASE REPORT

Phase:
PHASE_00_BOOTSTRAP

Status:
PASS / PARTIAL / FAIL

Objective:
<one sentence>

Plan Compliance:
PASS / PARTIAL / FAIL

Completed:
- ...
- ...
- ...

Files Created:
- ...
- ...
- ...

Resource Files Verified:
- Implementation plan: PASS/FAIL
- Initial prompt: PASS/FAIL
- Phase prompts: PASS/FAIL

Validation:
- <check>: PASS/FAIL
- <check>: PASS/FAIL

Tests Executed:
- ...

Problems:
- None
OR
- ...

Decisions:
- ...

Metrics:
- ...

Current State:
<one concise paragraph>

Next Phase:
PHASE_01_DATA

Next Phase Resource Prompt:
resources/prompts/PHASE_01_DATA.md

Recommended Next Action:
<one concise sentence>

Resume Instructions:
<exactly what the next agent should read/do first>
```

Do not provide a long explanation.

Do not propose additional features.

Do not continue implementation after this report.
