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

def test_rfm():
    conn = get_connection()
    with conn.cursor() as cur:
        with open('sql/analytics/rfm.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
        
        print("=== RFM Baseline ===")
        cur.execute(f"EXPLAIN (ANALYZE, BUFFERS) {sql}")
        for row in cur.fetchall():
            print(row[0])
            
        print("\n=== RFM without Seq Scan (Forcing Index Scan) ===")
        cur.execute("SET enable_seqscan = off;")
        cur.execute(f"EXPLAIN (ANALYZE, BUFFERS) {sql}")
        for row in cur.fetchall():
            print(row[0])
            
if __name__ == '__main__':
    test_rfm()
