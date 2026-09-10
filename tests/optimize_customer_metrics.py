import os
import psycopg2
from dotenv import load_dotenv
import time

def get_connection():
    load_dotenv()
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "postgres"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", ""),
    )

def test_query(conn, sql, name):
    print(f"=== {name} ===")
    with conn.cursor() as cur:
        # Run 3 times to warm cache
        for _ in range(3):
            cur.execute(sql)
            cur.fetchall()
            
        # Run EXPLAIN ANALYZE
        cur.execute(f"EXPLAIN (ANALYZE, BUFFERS) {sql}")
        for row in cur.fetchall():
            print(row[0])
            
        # Time multiple runs
        times = []
        for _ in range(5):
            start = time.time()
            cur.execute(sql)
            cur.fetchall()
            times.append(time.time() - start)
            
        print(f"Average Execution Time (cached): {sum(times)/len(times)*1000:.2f} ms\n")

if __name__ == '__main__':
    conn = get_connection()
    try:
        baseline_sql = """
        SELECT 
            c.customer_id,
            c.signup_date,
            c.city,
            c.age_group,
            c.gender,
            c.acquisition_channel,
            COUNT(t.transaction_id) AS transaction_count,
            COALESCE(SUM(t.amount), 0) AS total_revenue,
            COALESCE(SUM(t.amount) / NULLIF(COUNT(t.transaction_id), 0), 0) AS average_order_value,
            MIN(t.transaction_timestamp)::DATE AS first_purchase_date,
            MAX(t.transaction_timestamp)::DATE AS last_purchase_date,
            EXTRACT(DAY FROM (
                (SELECT MAX(transaction_timestamp) FROM transactions) - MAX(t.transaction_timestamp)
            )) AS days_since_last_purchase,
            CASE 
                WHEN COUNT(t.transaction_id) > 1 
                THEN EXTRACT(DAY FROM (MAX(t.transaction_timestamp) - MIN(t.transaction_timestamp))) / (COUNT(t.transaction_id) - 1)
                ELSE NULL 
            END AS purchase_frequency_days
        FROM customers c
        LEFT JOIN transactions t ON c.customer_id = t.customer_id
        GROUP BY 
            c.customer_id, 
            c.signup_date, 
            c.city, 
            c.age_group, 
            c.gender, 
            c.acquisition_channel
        ORDER BY total_revenue DESC;
        """

        optimized_sql = """
        WITH t_agg AS (
            SELECT 
                customer_id,
                COUNT(transaction_id) AS transaction_count,
                SUM(amount) AS total_revenue,
                MIN(transaction_timestamp) AS min_ts,
                MAX(transaction_timestamp) AS max_ts
            FROM transactions
            GROUP BY customer_id
        )
        SELECT 
            c.customer_id,
            c.signup_date,
            c.city,
            c.age_group,
            c.gender,
            c.acquisition_channel,
            COALESCE(t.transaction_count, 0) AS transaction_count,
            COALESCE(t.total_revenue, 0) AS total_revenue,
            COALESCE(t.total_revenue / NULLIF(t.transaction_count, 0), 0) AS average_order_value,
            t.min_ts::DATE AS first_purchase_date,
            t.max_ts::DATE AS last_purchase_date,
            EXTRACT(DAY FROM (
                (SELECT MAX(transaction_timestamp) FROM transactions) - t.max_ts
            )) AS days_since_last_purchase,
            CASE 
                WHEN t.transaction_count > 1 
                THEN EXTRACT(DAY FROM (t.max_ts - t.min_ts)) / (t.transaction_count - 1)
                ELSE NULL 
            END AS purchase_frequency_days
        FROM customers c
        LEFT JOIN t_agg t ON c.customer_id = t.customer_id
        ORDER BY t.total_revenue DESC NULLS LAST;
        """
        
        test_query(conn, baseline_sql, "Baseline customer_metrics")
        test_query(conn, optimized_sql, "Optimized customer_metrics (Pre-aggregation)")
        
    finally:
        conn.close()
