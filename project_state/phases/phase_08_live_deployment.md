# Phase 08 — Live Deployment Execution

Status: BLOCKED

Objective: Deploy the completed RetailPulse project to a real public environment and obtain a working public Streamlit URL.

Deployment Blocker:
External authentication/infrastructure blocks deployment.
The execution environment lacks an authenticated browser session for Streamlit Community Cloud and credentials for a hosted PostgreSQL provider (e.g. Supabase, Neon).

Required User Action:
The user must manually:
1. Create a hosted PostgreSQL database (e.g. Supabase, Neon) and run `database/schema.sql` and `database/seed.py` against it.
2. Sign in to Streamlit Community Cloud (via GitHub).
3. Connect the repository and configure the Streamlit Secrets (for the production database credentials).
4. Deploy the application.
