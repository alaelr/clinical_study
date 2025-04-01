from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import sys
import os


sys.path.insert(0, os.path.expanduser('/Users/alaelaroussi/Documents/Work/test_data_engineer/scripts')) 

default_args = {
    'owner': 'clinical_team',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'clinical_data_pipeline',
    default_args=default_args,
    description='Daily ETL for clinical data',
    schedule_interval='0 2 * * *',  # Runs at 2 AM daily
    catchup=False
)

# 1. ETL Task
run_etl = BashOperator(
    task_id='run_etl',
    bash_command='python /Users/alaelaroussi/Documents/Work/test_data_engineer/scripts/etl.py',
    dag=dag
)

# 2. PostgreSQL Load Task
load_postgres = BashOperator(
    task_id='load_postgresql',
    bash_command='python /Users/alaelaroussi/Documents/Work/test_data_engineer/scripts/load_postgresql.py',
    dag=dag
)

# 3. Supabase Migration Task
migrate_supabase = BashOperator(
    task_id='migrate_to_supabase',
    bash_command='python /Users/alaelaroussi/Documents/Work/test_data_engineer/scripts/migrate_to_supabase.py',
    dag=dag
)

# Set task dependencies
run_etl >> load_postgres >> migrate_supabase