# PHASE 05 — Streamlit Application

## Objective

Build a functional Streamlit dashboard that displays all analytical results from Phase 3, connects to PostgreSQL, and uses appropriate caching.

## Scope

- Single-page Streamlit application
- All KPI, RFM, cohort, category, and concentration analytics displayed
- PostgreSQL connection
- Caching for queries and connections
- Functional over polished

## Inputs

- Populated PostgreSQL database from Phase 2
- SQL queries from Phase 3
- `src/analytics.py` from Phase 3
- `resources/IMPLEMENTATION_PLAN.md` — Streamlit application requirements section

## Required Implementation Tasks

1. Create/update `app/streamlit_app.py`:
   - Page title: "RetailPulse — Customer Retention & Revenue Intelligence"
   - KPI metric cards at top: Total Revenue, Active Customers, Repeat Purchase Rate, AOV
   - Revenue trend chart (time series line chart)
   - RFM segment distribution (bar or pie chart)
   - Cohort retention heatmap
   - Revenue by category chart
   - Revenue concentration visualization
   - Top customers table

2. Ensure `src/analytics.py` provides all required data functions

3. Ensure `src/db.py` provides database connection with:
   - `@st.cache_resource` for connection/engine
   - Error handling for connection failures

4. Ensure `src/config.py` reads from environment variables and Streamlit secrets

5. Use `@st.cache_data` for all analytical query results

6. Add filters if time permits:
   - Date range filter
   - Category filter
   - Segment filter

## Required Files

```
app/streamlit_app.py
src/analytics.py (update if needed)
src/db.py (update if needed)
src/config.py (update if needed)
```

## Validation Checks

- [ ] `streamlit run app/streamlit_app.py` starts without errors
- [ ] KPI cards display correct values
- [ ] Revenue trend chart renders
- [ ] RFM segment chart renders
- [ ] Cohort retention heatmap renders
- [ ] Category chart renders
- [ ] Top customers table renders
- [ ] Database connection works
- [ ] Caching is implemented (@st.cache_data, @st.cache_resource)
- [ ] No hardcoded database credentials

## Expected Outputs

- Working Streamlit application displaying all analytics
- Locally runnable dashboard

## Definition of Done

Streamlit application runs locally, connects to PostgreSQL, displays all required analytical sections with proper caching. No hardcoded secrets.

## Handoff Requirements

- Application runs with `streamlit run app/streamlit_app.py`
- All analytical sections display correctly
- Ready for deployment in Phase 6
- STATE.md updated

## STOP INSTRUCTION

**Do NOT execute PHASE 6 after completing PHASE 5.**

Stop after producing the Phase 5 completion report. Wait for explicit user instruction to proceed.
