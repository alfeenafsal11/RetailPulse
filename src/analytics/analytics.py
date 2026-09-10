import pandas as pd
from .db import get_connection
from .queries import (
    KPI_QUERY,
    CUSTOMER_METRICS_QUERY,
    RFM_QUERY,
    COHORTS_QUERY,
    CATEGORY_ANALYSIS_QUERY,
    REVENUE_CONCENTRATION_QUERY,
    TOP_CUSTOMERS_QUERY
)

def _execute_query(query: str) -> pd.DataFrame:
    """Executes a SQL query and returns a pandas DataFrame."""
    conn = get_connection()
    try:
        return pd.read_sql(query, conn)
    finally:
        conn.close()

def load_kpis():
    """
    Loads overall KPIs and time-series revenue trends.
    kpis.sql contains two statements separated by ';'.
    """
    queries = [q.strip() for q in KPI_QUERY.split(';') if q.strip()]
    overall_kpi_query = queries[0]
    time_series_query = queries[1]
    
    overall_df = _execute_query(overall_kpi_query)
    time_series_df = _execute_query(time_series_query)
    
    # Ensure types
    for col in ['total_revenue', 'average_order_value', 'repeat_purchase_rate']:
        overall_df[col] = pd.to_numeric(overall_df[col], errors='coerce')
        
    time_series_df['monthly_revenue'] = pd.to_numeric(time_series_df['monthly_revenue'])
    time_series_df['txn_month'] = pd.to_datetime(time_series_df['txn_month'])
    
    return {
        'overall': overall_df,
        'time_series': time_series_df
    }

def load_customer_metrics() -> pd.DataFrame:
    """Loads customer metrics and converts types."""
    df = _execute_query(CUSTOMER_METRICS_QUERY)
    df['total_revenue'] = pd.to_numeric(df['total_revenue'])
    df['average_order_value'] = pd.to_numeric(df['average_order_value'])
    return df

def load_rfm():
    """
    Loads RFM scores and segments, and creates a summary.
    """
    df = _execute_query(RFM_QUERY)
    df['total_revenue'] = pd.to_numeric(df['total_revenue'])
    df['avg_revenue_per_customer'] = pd.to_numeric(df['avg_revenue_per_customer'])
    df['avg_recency_days'] = pd.to_numeric(df['avg_recency_days'])
    df['avg_frequency'] = pd.to_numeric(df['avg_frequency'])
    
    # Optional: order categories for UI presentation
    segment_order = ['Champions', 'Loyal', 'New', 'At Risk', 'Lost', 'Other']
    df['rfm_segment'] = pd.Categorical(df['rfm_segment'], categories=segment_order, ordered=True)
    df = df.sort_values('rfm_segment')
    
    return df

def load_cohorts():
    """
    Loads cohort retention data and pivots it into a heatmap format.
    """
    df = _execute_query(COHORTS_QUERY)
    df['retention_rate_pct'] = pd.to_numeric(df['retention_rate_pct'])
    df['cohort_month'] = pd.to_datetime(df['cohort_month'])
    
    # Pivot into heatmap format: rows=cohort_month, cols=months_since, vals=retention_rate_pct
    heatmap_df = df.pivot(index='cohort_month', columns='months_since_first_purchase', values='retention_rate_pct')
    
    return {
        'raw': df,
        'heatmap': heatmap_df
    }

def load_category_analysis() -> pd.DataFrame:
    """Loads category performance data."""
    df = _execute_query(CATEGORY_ANALYSIS_QUERY)
    df['total_revenue'] = pd.to_numeric(df['total_revenue'])
    df['average_transaction_value'] = pd.to_numeric(df['average_transaction_value'])
    return df

def load_revenue_concentration() -> pd.DataFrame:
    """Loads revenue concentration by customer percentiles."""
    df = _execute_query(REVENUE_CONCENTRATION_QUERY)
    df['band_revenue'] = pd.to_numeric(df['band_revenue'])
    df['total_revenue'] = pd.to_numeric(df['total_revenue'])
    df['pct_of_total_revenue'] = pd.to_numeric(df['pct_of_total_revenue'])
    
    # Order bands correctly based on band_order already in SQL, but just in case
    # we don't need to do much because SQL already ordered it by band_order.
    return df

def load_top_customers() -> pd.DataFrame:
    """Loads top 20 customers."""
    df = _execute_query(TOP_CUSTOMERS_QUERY)
    df['total_revenue'] = pd.to_numeric(df['total_revenue'])
    df['average_order_value'] = pd.to_numeric(df['average_order_value'])
    return df

def load_all_analytics():
    """
    Loads all datasets for the dashboard.
    """
    return {
        'kpis': load_kpis(),
        'customer_metrics': load_customer_metrics(),
        'rfm': load_rfm(),
        'cohorts': load_cohorts(),
        'categories': load_category_analysis(),
        'concentration': load_revenue_concentration(),
        'top_customers': load_top_customers()
    }
