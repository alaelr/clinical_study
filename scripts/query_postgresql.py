import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from pathlib import Path
import logging
import sys

from typing import Optional, Tuple, List, Any

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('database.log')
    ]
)
logger = logging.getLogger(__name__)

# Database connection parameters
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "application_name": os.getenv("APP_NAME"),
    "connect_timeout": 5
}

def get_connection():
    """Establish and return a PostgreSQL connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = False
        logger.info(f"Connected to {DB_CONFIG['dbname']} successfully")
        return conn
    except psycopg2.Error as e:
        logger.error(f"Connection failed to {DB_CONFIG['dbname']}")
        logger.error(f"Error details: {e}")
        raise

def execute_query(conn, query, params=None):
    """Execute a SQL query and return results as DataFrame"""
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                data = cursor.fetchall()
                return (columns, data)
            return (None, None)
    except psycopg2.Error as e:
        conn.rollback()
        logger.error(f"Query failed: {e}")
        raise

def execute_query_from_file(conn, file_path):
    """Execute SQL query from file"""
    try:
        with open(file_path, 'r') as f:
            query = f.read()
        return execute_query(conn, query)
    except Exception as e:
        logger.error(f"File read error: {e}")
        raise

# Test connection when module loads
try:
    test_conn = get_connection()
    test_conn.close()
except ImportError:
    pass  # Allow module to be imported for testing