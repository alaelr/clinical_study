from query_postgresql import get_connection, execute_query, execute_query_from_file
from pathlib import Path
import pandas as pd



conn = get_connection()

query_path = Path(__file__).parent.parent / "sql_queries" / "sort_pation_by_diagnosis.sql"
columns, data = execute_query_from_file(conn, query_path)

df = pd.DataFrame(data, columns=columns)
df.to_csv('/Users/alaelaroussi/Documents/Work/test_data_engineer/output/sort_pation_by_diagnosis.csv', index=False)

print("Query executed and data saved to CSV.")