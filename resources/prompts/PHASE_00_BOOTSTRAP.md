# PHASE 00 — Bootstrap

## Objective

Create the minimal repository structure, implementation-plan resources, phase prompts, and persistent project-state infrastructure required for controlled multi-phase development.

## Scope

- Repository skeleton (directories, config files)
- Resource files (implementation plan, initial prompt, all phase prompts)
- Project state infrastructure (STATE.md, EVENTS.md, DECISIONS.md, METRICS.md, phase files)
- Git initialization
- No application code

## Inputs

- User's initial prompt and implementation plan references
- This protocol document

## Required Implementation Tasks

1. Initialize git repository
2. Create `.gitignore` for Python/PostgreSQL/Streamlit project
3. Create `README.md` with project objective and planned architecture
4. Create `AGENTS.md` with agent operating rules
5. Create `requirements.txt` with minimal dependencies
6. Create directory structure:
   - `data/raw/`, `data/processed/`
   - `database/`
   - `sql/`, `sql/performance/`
   - `src/`
   - `app/`
   - `tests/`
   - `resources/`, `resources/prompts/`
   - `project_state/`, `project_state/phases/`
7. Create `resources/IMPLEMENTATION_PLAN.md` covering all phases
8. Create `resources/INITIAL_PROMPT.md` preserving the originating instruction
9. Create all 8 phase prompt files in `resources/prompts/`
10. Create `project_state/STATE.md`
11. Create `project_state/EVENTS.md`
12. Create `project_state/DECISIONS.md`
13. Create `project_state/METRICS.md`
14. Create all 8 phase files in `project_state/phases/`

## Required Files

```
README.md
AGENTS.md
requirements.txt
.gitignore
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
project_state/STATE.md
project_state/EVENTS.md
project_state/DECISIONS.md
project_state/METRICS.md
project_state/phases/phase_00_bootstrap.md
project_state/phases/phase_01_data.md
project_state/phases/phase_02_database.md
project_state/phases/phase_03_analytics.md
project_state/phases/phase_04_performance.md
project_state/phases/phase_05_app.md
project_state/phases/phase_06_deployment.md
project_state/phases/phase_07_final.md
```

## Validation Checks

- [ ] All directories exist
- [ ] All resource files exist and are non-empty
- [ ] All state files exist and are non-empty
- [ ] All phase files exist and are non-empty
- [ ] Implementation plan covers PHASE 0–7
- [ ] Each phase prompt contains: scope, tasks, validation, definition of done, stop instruction
- [ ] Resource files do not contradict one another
- [ ] No unnecessary dependencies in requirements.txt
- [ ] Git repository initialized
- [ ] No secrets present
- [ ] README contains project objective and architecture
- [ ] No application code was created
- [ ] STATE.md documents current phase as PHASE 0

## Expected Outputs

- Complete repository skeleton
- Coherent set of resource files
- Initialized project state infrastructure
- Git repository ready for Phase 1

## Definition of Done

All files listed above exist, are coherent with each other, and pass all validation checks. No application code has been created. The project is ready for Phase 1 execution.

## Handoff Requirements

- STATE.md shows PHASE 0 COMPLETE, next phase PHASE 1
- Phase file phase_00_bootstrap.md is fully updated
- EVENTS.md contains PHASE_STARTED and PHASE_COMPLETED entries
- DECISIONS.md contains initial architectural decisions
- All resource files are internally consistent

## STOP INSTRUCTION

**Do NOT execute PHASE 1 after completing PHASE 0.**

Stop after producing the Phase 0 completion report. Wait for explicit user instruction to proceed.
