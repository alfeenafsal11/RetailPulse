import os

def load_sql_query(filename):
    """
    Loads a SQL query string from the sql/analytics directory.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    filepath = os.path.join(base_dir, 'sql', 'analytics', filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"SQL file not found at {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        # In case the file has multiple statements separated by ';',
        # we might need to handle it. However, psycopg2 execute with Pandas 
        # usually prefers single queries or we split them if needed. 
        # For now, returning the raw string.
        return f.read()

# Query Constants
KPI_QUERY = load_sql_query('kpis.sql')
CUSTOMER_METRICS_QUERY = load_sql_query('customer_metrics.sql')
RFM_QUERY = load_sql_query('rfm.sql')
COHORTS_QUERY = load_sql_query('cohorts.sql')
CATEGORY_ANALYSIS_QUERY = load_sql_query('category_analysis.sql')
REVENUE_CONCENTRATION_QUERY = load_sql_query('revenue_concentration.sql')
TOP_CUSTOMERS_QUERY = load_sql_query('top_customers.sql')
