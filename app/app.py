import os
import sys
import streamlit as st
import plotly.express as px
import pandas as pd

# Ensure src is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

try:
    from analytics.analytics import load_all_analytics
except ImportError as e:
    st.error(f"Failed to import analytics module. Please ensure you are running from the project root. Error: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="RetailPulse | Customer Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.title("RetailPulse")
st.subheader("Customer Retention & Revenue Analytics")
st.markdown("This dashboard provides a comprehensive view of retail performance, focusing on customer segmentation, retention, and revenue concentration.")

# Data Loading
@st.cache_data(ttl=3600)
def get_data():
    try:
        return load_all_analytics()
    except Exception as e:
        st.error("🚨 Failed to connect to the PostgreSQL database or execute analytics queries.")
        st.error(f"Details: {e}")
        st.info("Please ensure PostgreSQL is running and environment variables are properly configured in `.env`.")
        st.stop()

with st.spinner("Loading analytical datasets..."):
    datasets = get_data()

# Validate datasets
required_keys = ['kpis', 'customer_metrics', 'rfm', 'cohorts', 'categories', 'concentration', 'top_customers']
missing_keys = [k for k in required_keys if k not in datasets]
if missing_keys:
    st.error(f"Missing required analytical datasets: {missing_keys}")
    st.stop()

# Extract datasets
overall_kpi = datasets['kpis']['overall'].iloc[0]
time_series_kpi = datasets['kpis']['time_series']
customer_metrics = datasets['customer_metrics']
rfm_summary = datasets['rfm']
cohorts_heatmap = datasets['cohorts']['heatmap']
category_df = datasets['categories']
concentration_df = datasets['concentration']
top_customers_df = datasets['top_customers']

st.markdown("---")

# 1. KPIs
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Revenue", f"${overall_kpi['total_revenue']:,.2f}")
with col2:
    st.metric("Active Customers", f"{overall_kpi['active_customers']:,}")
with col3:
    st.metric("Total Transactions", f"{overall_kpi['total_transactions']:,}")
with col4:
    st.metric("Average Order Value", f"${overall_kpi['average_order_value']:,.2f}")
with col5:
    st.metric("Repeat Purchase Rate", f"{overall_kpi['repeat_purchase_rate']*100:.2f}%")

st.markdown("---")

# 2. Monthly Revenue Trend
st.subheader("Monthly Revenue Trend")
fig_trend = px.line(
    time_series_kpi, x='txn_month', y='monthly_revenue', 
    title="Revenue over Time",
    labels={'txn_month': 'Month', 'monthly_revenue': 'Revenue ($)'},
    markers=True
)
fig_trend.update_yaxes(tickprefix="$")
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")

# 3. Category & RFM
col_cat, col_rfm = st.columns(2)

with col_cat:
    st.subheader("Revenue by Category")
    fig_cat = px.bar(
        category_df, x='category_name', y='total_revenue',
        title="Revenue Contribution by Product Category",
        labels={'category_name': 'Category', 'total_revenue': 'Revenue ($)'},
        color='total_revenue', color_continuous_scale='Blues'
    )
    fig_cat.update_yaxes(tickprefix="$")
    st.plotly_chart(fig_cat, use_container_width=True)
    
with col_rfm:
    st.subheader("RFM Customer Segmentation")
    st.markdown("*RFM segmentation identifies customers based on observed purchasing behavior (Recency, Frequency, Monetary).*")
    # 'Other' is a legitimate catch-all category for middle-tier customers not hitting extreme boundaries.
    fig_rfm = px.bar(
        rfm_summary, x='rfm_segment', y='segment_size',
        title="Customer Count by RFM Segment",
        labels={'rfm_segment': 'Segment', 'segment_size': 'Customers'},
        color='rfm_segment',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig_rfm, use_container_width=True)
    
    st.markdown("**Segment Revenue Summary**")
    st.dataframe(
        rfm_summary[['rfm_segment', 'segment_size', 'total_revenue', 'avg_revenue_per_customer']].style.format({
            'total_revenue': '${:,.2f}',
            'avg_revenue_per_customer': '${:,.2f}'
        }),
        use_container_width=True, hide_index=True
    )

st.markdown("---")

# 4. Cohort Retention
st.subheader("Cohort Retention")
st.markdown("*Retention is measured relative to each customer's first observed purchase month.*")

# Using plotly express imshow for heatmap
# Reset index for better display if needed, but cohort_month index is fine
# Convert the index to string (YYYY-MM) for cleaner y-axis
heatmap_display = cohorts_heatmap.copy()
heatmap_display.index = heatmap_display.index.strftime('%Y-%m')

fig_cohort = px.imshow(
    heatmap_display,
    labels=dict(x="Months Since First Purchase", y="Cohort Month", color="Retention Rate (%)"),
    x=heatmap_display.columns,
    y=heatmap_display.index,
    color_continuous_scale='Blues',
    aspect="auto"
)
fig_cohort.update_layout(xaxis_nticks=len(heatmap_display.columns))
st.plotly_chart(fig_cohort, use_container_width=True)

st.markdown("---")

# 5. Revenue Concentration
st.subheader("Revenue Concentration")
st.markdown("*This shows how cumulative customer revenue changes as progressively larger portions of the customer base are included.*")

fig_conc = px.line(
    concentration_df, x='band_name', y='pct_of_total_revenue',
    title="Revenue Contribution by Customer Percentile",
    labels={'band_name': 'Customer Percentile', 'pct_of_total_revenue': 'Cumulative Revenue Share (%)'},
    markers=True
)
fig_conc.update_yaxes(ticksuffix="%")
st.plotly_chart(fig_conc, use_container_width=True)

st.markdown("---")

# 6. Top Customers & Explorer
col_top, col_exp = st.columns(2)

with col_top:
    st.subheader("Top 20 Customers")
    st.dataframe(
        top_customers_df[['customer_id', 'total_revenue', 'transaction_count', 'average_order_value', 'last_purchase_date']].style.format({
            'total_revenue': '${:,.2f}',
            'average_order_value': '${:,.2f}'
        }),
        use_container_width=True, hide_index=True
    )

with col_exp:
    st.subheader("Customer Explorer")
    st.markdown("*Select a Customer ID to view their lifetime metrics.*")
    
    # Simple search or selectbox
    selected_customer = st.selectbox(
        "Search Customer ID",
        options=customer_metrics['customer_id'].unique(),
        index=0
    )
    
    cust_data = customer_metrics[customer_metrics['customer_id'] == selected_customer].iloc[0]
    
    st.metric("Total Revenue", f"${cust_data['total_revenue']:,.2f}")
    st.metric("Transaction Count", f"{cust_data['transaction_count']}")
    st.metric("Average Order Value", f"${cust_data['average_order_value']:,.2f}")
    st.metric("First Purchase Date", f"{cust_data['first_purchase_date']}")
    st.metric("Last Purchase Date", f"{cust_data['last_purchase_date']}")
    st.metric("Days Since Last Purchase", f"{cust_data['days_since_last_purchase']}")
