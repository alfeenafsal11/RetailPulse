import os
import psycopg2
from dotenv import load_dotenv

def get_connection():
    load_dotenv()
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "postgres"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", ""),
    )

def execute_sql_file(conn, filename, fetch=True):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sql', 'analytics', filename)
    with open(path, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    with conn.cursor() as cur:
        # If the file has multiple statements, we only fetch the last one if it's a SELECT.
        # But our files are single logical queries (possibly with CTEs).
        cur.execute(sql)
        if fetch:
            columns = [desc[0] for desc in cur.description] if cur.description else []
            results = cur.fetchall()
            return columns, results
    return [], []

def validate_analytics(conn):
    print("--- Phase 3: Analytical SQL Execution and Validation ---\n")
    
    # 1. KPIs
    cols, results = execute_sql_file(conn, 'kpis.sql')
    # First query in kpis.sql is overall_kpis, second is time-series.
    # psycopg2 cur.execute on multiple statements executes all, but cur.fetchall() only gets the LAST query.
    # To fix this in testing, I will split the file manually by ';' or just query what we need.
    pass

def execute_single_queries(conn):
    path_kpis = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sql', 'analytics', 'kpis.sql')
    with open(path_kpis, 'r', encoding='utf-8') as f:
        kpi_sql = f.read().split(';')
    
    with conn.cursor() as cur:
        # Query 1: KPIs
        cur.execute(kpi_sql[0])
        kpi_row = cur.fetchone()
        if kpi_row:
            total_revenue = kpi_row[0]
            active_customers = kpi_row[1]
            total_transactions = kpi_row[2]
            aov = kpi_row[3]
            repeat_rate = kpi_row[4]
            print(f"KPIs:")
            print(f"  Total Revenue: ${total_revenue:,.2f}")
            print(f"  Active Customers: {active_customers:,}")
            print(f"  Total Transactions: {total_transactions:,}")
            print(f"  AOV: ${aov:,.2f}")
            print(f"  Repeat Purchase Rate: {repeat_rate*100:.2f}%")
        
    print("\nExecuting customer metrics...")
    cols, cust_results = execute_sql_file(conn, 'customer_metrics.sql')
    print(f"  Rows returned: {len(cust_results)}")
    cust_rev = sum(row[7] for row in cust_results) # index 7 is total_revenue
    print(f"  Customer Revenue Sum: ${cust_rev:,.2f}")
    assert abs(cust_rev - total_revenue) < 1.0, "Customer revenue does not match total revenue!"
    
    print("\nExecuting RFM...")
    cols, rfm_results = execute_sql_file(conn, 'rfm.sql')
    print("  RFM Segments:")
    total_rfm_rev = 0
    total_rfm_custs = 0
    for row in rfm_results:
        segment, size, rev, avg_rev, txns, avg_rec, avg_freq = row
        print(f"    {segment}: {size:,} customers, ${rev:,.2f} revenue")
        total_rfm_rev += rev
        total_rfm_custs += size
    assert abs(total_rfm_rev - total_revenue) < 1.0, "RFM revenue does not match total revenue!"
    assert total_rfm_custs == active_customers, "RFM customer count does not match active customers!"

    print("\nExecuting Category Analysis...")
    cols, cat_results = execute_sql_file(conn, 'category_analysis.sql')
    print(f"  Categories:")
    cat_rev_sum = 0
    for row in cat_results:
        cat, rev, txns, units, aov2 = row
        print(f"    {cat}: ${rev:,.2f} ({txns:,} txns)")
        cat_rev_sum += rev
    assert abs(cat_rev_sum - total_revenue) < 1.0, "Category revenue does not match total revenue!"
    
    print("\nExecuting Revenue Concentration...")
    cols, conc_results = execute_sql_file(conn, 'revenue_concentration.sql')
    print("  Concentration:")
    for row in conc_results:
        band, c_count, b_rev, t_rev, pct = row
        print(f"    {band}: {c_count:,} customers -> {pct}% of revenue")
        
    print("\nExecuting Cohorts (sample output)...")
    cols, cohort_results = execute_sql_file(conn, 'cohorts.sql')
    print(f"  Returned {len(cohort_results)} cohort-month rows.")
    if cohort_results:
         print(f"  First row: {cohort_results[0]}")
         
    # Validate Join Integrity
    print("\nValidating Join Integrity...")
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM transactions t JOIN customers c ON t.customer_id = c.customer_id")
        txn_c_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM transactions t JOIN products p ON t.product_id = p.product_id")
        txn_p_count = cur.fetchone()[0]
        
    assert txn_c_count == total_transactions, f"Customer join multiplied rows! Expected {total_transactions}, got {txn_c_count}"
    assert txn_p_count == total_transactions, f"Product join multiplied rows! Expected {total_transactions}, got {txn_p_count}"
    print("  Join integrity: PASS (Transaction count preserved)")
    
    print("\nAll analytical queries executed and validated successfully.")

if __name__ == '__main__':
    conn = get_connection()
    try:
         execute_single_queries(conn)
    finally:
         conn.close()
