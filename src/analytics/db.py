import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

def get_connection():
    """
    Establish a connection to the PostgreSQL database using environment variables.
    """
    load_dotenv()
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_NAME", "postgres"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "")
    )
