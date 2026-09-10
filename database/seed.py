import os
import psycopg2
import time
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

def init_schema(conn):
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path, "r") as f:
        schema_sql = f.read()
    
    with conn.cursor() as cur:
        # Drop tables if they exist for idempotency
        cur.execute("DROP TABLE IF EXISTS transactions;")
        cur.execute("DROP TABLE IF EXISTS products;")
        cur.execute("DROP TABLE IF EXISTS customers;")
        
        # Execute the schema
        cur.execute(schema_sql)
    conn.commit()
    print("Schema initialized successfully.")

def bulk_load(conn):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    raw_dir = os.path.join(base_dir, "data", "raw")
    
    tables = [
        ("customers", "customers.csv"),
        ("products", "products.csv"),
        ("transactions", "transactions.csv")
    ]
    
    with conn.cursor() as cur:
        for table_name, file_name in tables:
            file_path = os.path.join(raw_dir, file_name)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Missing data file: {file_path}")
            
            print(f"Loading {table_name} from {file_name}...")
            start_time = time.time()
            
            with open(file_path, "r", encoding="utf-8") as f:
                # COPY statement for bulk insert (skip header)
                sql = f"COPY {table_name} FROM STDIN WITH CSV HEADER"
                cur.copy_expert(sql, f)
            
            elapsed = time.time() - start_time
            
            cur.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cur.fetchone()[0]
            print(f"  -> Loaded {count:,} rows in {elapsed:.2f}s")
            
    conn.commit()

def validate_data(conn):
    print("\nRunning database validation...")
    with conn.cursor() as cur:
        # 1. Total Transaction Count
        cur.execute("SELECT COUNT(*) FROM transactions;")
        txn_count = cur.fetchone()[0]
        print(f"Total Transactions: {txn_count:,}")
        
        # 2. Total Revenue
        cur.execute("SELECT SUM(amount) FROM transactions;")
        total_rev = cur.fetchone()[0]
        print(f"Total Revenue: ${total_rev:,.2f}")
        
        # 3. Revenue by category
        cur.execute("""
            SELECT p.category, SUM(t.amount) as rev 
            FROM transactions t
            JOIN products p ON t.product_id = p.product_id
            GROUP BY p.category
            ORDER BY rev DESC;
        """)
        print("Revenue by Category:")
        for row in cur.fetchall():
            print(f"  {row[0]}: ${row[1]:,.2f}")

        # 4. Earliest and Latest Timestamps
        cur.execute("SELECT MIN(transaction_timestamp), MAX(transaction_timestamp) FROM transactions;")
        min_ts, max_ts = cur.fetchone()
        print(f"Date Range: {min_ts} to {max_ts}")

if __name__ == "__main__":
    print("Connecting to PostgreSQL...")
    conn = get_connection()
    try:
        init_schema(conn)
        bulk_load(conn)
        validate_data(conn)
        print("\nPhase 2 Database Loading Complete.")
    finally:
        conn.close()
