import pytest
from scripts.query_postgresql import get_connection, execute_query, execute_query_from_file
import os
from pathlib import Path

@pytest.fixture(scope="module")
def db_connection():
    """Fixture providing database connection"""
    conn = get_connection()
    yield conn
    conn.close()

def test_connection(db_connection):
    """Test database connection is active"""
    assert not db_connection.closed, "Connection is closed"

def test_patients_table_exists(db_connection):
    """Verify patients table exists and is accessible"""
    columns, data = execute_query(db_connection, "SELECT * FROM patients LIMIT 1")
    assert columns, "No columns returned"  # Checks if columns list exists
    assert 'patient_id' in columns, "patient_id column missing"

def test_visits_query(db_connection):
    """Test visits query from file"""
    query_path = Path(__file__).parent.parent / "sql_queries" / "visits_for_patient.sql"
    columns, data = execute_query_from_file(db_connection, query_path)
    assert len(columns) > 0, "No columns returned"
    assert len(data) >= 0, "Negative row count"
