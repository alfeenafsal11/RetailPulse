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

def run_explain(conn, sql_path):
    with open(sql_path, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    print(f"=== EXPLAIN ANALYZE for {os.path.basename(sql_path)} ===")
    with conn.cursor() as cur:
        # We wrap the query in EXPLAIN ANALYZE BUFFERS VERBOSE
        explain_query = f"EXPLAIN (ANALYZE, BUFFERS) {sql}"
        cur.execute(explain_query)
        for row in cur.fetchall():
            print(row[0])
    print("=" * 80 + "\n")

if __name__ == '__main__':
    conn = get_connection()
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        run_explain(conn, os.path.join(base_dir, 'sql', 'analytics', 'rfm.sql'))
        run_explain(conn, os.path.join(base_dir, 'sql', 'analytics', 'customer_metrics.sql'))
        run_explain(conn, os.path.join(base_dir, 'sql', 'analytics', 'revenue_concentration.sql'))
    finally:
        conn.close()
