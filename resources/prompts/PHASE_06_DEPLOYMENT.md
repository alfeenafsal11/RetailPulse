# PHASE 06 — Public Deployment

## Objective

Deploy the Streamlit application publicly so it is accessible from an external browser via a public URL.

## Scope

- Cloud PostgreSQL provisioning
- Streamlit Cloud deployment
- Secrets configuration
- Public URL verification

## Inputs

- Working Streamlit application from Phase 5
- `requirements.txt`
- Database schema and data from Phase 2
- `resources/IMPLEMENTATION_PLAN.md` — deployment requirements section

## Required Implementation Tasks

1. Provision cloud PostgreSQL:
   - Use a free-tier provider (Neon, Supabase, Railway, or equivalent)
   - Create database and schema
   - Load data
   - Verify connectivity

2. Configure Streamlit Cloud deployment:
   - Ensure `requirements.txt` is deployment-ready
   - Configure Streamlit secrets for database connection
   - Set up repository connection to Streamlit Cloud
   - Deploy application

3. Verify deployment:
   - Access application from public URL
   - Verify all dashboard sections load
   - Verify database connectivity from cloud
   - Test from external browser (not localhost)

4. Update project files:
   - Add deployment URL to README.md
   - Record deployment status in STATE.md
   - Record deployment URL in METRICS.md

## Required Files

```
requirements.txt (verify deployment-ready)
.streamlit/config.toml (if needed)
```

## Validation Checks

- [ ] Cloud database is accessible
- [ ] Cloud database contains all data
- [ ] Streamlit Cloud deployment succeeds
- [ ] Application is accessible from public URL
- [ ] All dashboard sections render on deployed app
- [ ] No secrets in git repository
- [ ] Deployment URL documented in README
- [ ] Deployment URL documented in STATE.md

## Expected Outputs

- Publicly accessible Streamlit application
- Cloud PostgreSQL database
- Deployment URL

## Definition of Done

Application is live at a public URL. All dashboard sections work on the deployed version. Database is accessible from the cloud. No secrets are committed to git.

## Handoff Requirements

- Public URL recorded
- Deployment verified from external browser
- STATE.md updated with deployment URL
- Ready for final validation in Phase 7

## STOP INSTRUCTION

**Do NOT execute PHASE 7 after completing PHASE 6.**

Stop after producing the Phase 6 completion report. Wait for explicit user instruction to proceed.
