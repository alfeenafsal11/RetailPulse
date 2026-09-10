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

def test_query(conn, sql, name):
    print(f"=== {name} ===")
    with conn.cursor() as cur:
        cur.execute(f"EXPLAIN (ANALYZE, BUFFERS) {sql}")
        for row in cur.fetchall():
            print(row[0])

if __name__ == '__main__':
    conn = get_connection()
    try:
        baseline_sql = """
        WITH customer_cohorts AS (
            SELECT customer_id, DATE_TRUNC('month', MIN(transaction_timestamp)) AS cohort_month
            FROM transactions GROUP BY customer_id
        ),
        customer_activities AS (
            SELECT DISTINCT customer_id, DATE_TRUNC('month', transaction_timestamp) AS activity_month
            FROM transactions
        ),
        cohort_retention AS (
            SELECT c.cohort_month, a.activity_month, c.customer_id,
                EXTRACT(YEAR FROM age(a.activity_month, c.cohort_month)) * 12 + 
                EXTRACT(MONTH FROM age(a.activity_month, c.cohort_month)) AS months_since_first_purchase
            FROM customer_cohorts c JOIN customer_activities a ON c.customer_id = a.customer_id
        ),
        cohort_sizes AS (
            SELECT cohort_month, COUNT(DISTINCT customer_id) AS cohort_size
            FROM customer_cohorts GROUP BY cohort_month
        )
        SELECT r.cohort_month::DATE AS cohort_month, s.cohort_size, r.months_since_first_purchase,
            COUNT(DISTINCT r.customer_id) AS retained_customers,
            ROUND((COUNT(DISTINCT r.customer_id)::NUMERIC / s.cohort_size::NUMERIC) * 100, 2) AS retention_rate_pct
        FROM cohort_retention r JOIN cohort_sizes s ON r.cohort_month = s.cohort_month
        GROUP BY r.cohort_month, s.cohort_size, r.months_since_first_purchase
        ORDER BY r.cohort_month, r.months_since_first_purchase;
        """

        optimized_sql = """
        WITH customer_cohorts AS (
            SELECT customer_id, DATE_TRUNC('month', MIN(transaction_timestamp)) AS cohort_month
            FROM transactions GROUP BY customer_id
        ),
        customer_activities AS (
            SELECT customer_id, DATE_TRUNC('month', transaction_timestamp) AS activity_month
            FROM transactions GROUP BY customer_id, DATE_TRUNC('month', transaction_timestamp)
        ),
        cohort_retention AS (
            SELECT c.cohort_month, a.activity_month, c.customer_id,
                EXTRACT(YEAR FROM age(a.activity_month, c.cohort_month)) * 12 + 
                EXTRACT(MONTH FROM age(a.activity_month, c.cohort_month)) AS months_since_first_purchase
            FROM customer_cohorts c JOIN customer_activities a ON c.customer_id = a.customer_id
        ),
        cohort_sizes AS (
            SELECT cohort_month, COUNT(DISTINCT customer_id) AS cohort_size
            FROM customer_cohorts GROUP BY cohort_month
        )
        SELECT r.cohort_month::DATE AS cohort_month, s.cohort_size, r.months_since_first_purchase,
            COUNT(DISTINCT r.customer_id) AS retained_customers,
            ROUND((COUNT(DISTINCT r.customer_id)::NUMERIC / s.cohort_size::NUMERIC) * 100, 2) AS retention_rate_pct
        FROM cohort_retention r JOIN cohort_sizes s ON r.cohort_month = s.cohort_month
        GROUP BY r.cohort_month, s.cohort_size, r.months_since_first_purchase
        ORDER BY r.cohort_month, r.months_since_first_purchase;
        """
        test_query(conn, baseline_sql, "Baseline cohorts")
        test_query(conn, optimized_sql, "Optimized cohorts (GROUP BY)")
        
    finally:
        conn.close()
