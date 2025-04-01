# Patient Data ETL Pipeline

This project is a simple ETL (Extract, Transform, Load) pipeline for processing patient-related data. It reads multiple CSV files, cleans and transforms the data, and merges them into a final dataset.

## Project Structure

test_data_engineer/
   ├── .env # Environment variables (database credentials)
   ├── .gitignore # Files to exclude from version control
   ├── requirements.txt # Python dependencies
   │
   ├── airflow/ # Airflow DAGs directory
   │ └── dags/
   │ └── clinical_etl_pipeline.py # Main Airflow pipeline
   │
   ├── data/ # Raw input data files
   │ ├── patient_demographics.csv
   │ ├── patient_lab_results.csv
   │ ├── patient_medications.csv
   │ ├── patient_visits.csv
   │ └── physician_assignments.csv
   │
   ├── output/ # Processed output files
   │ └── cleaned_patient_data.csv
   │
   ├── scripts/ # Data processing scripts
   │ ├── init.py # Python package marker
   │ ├── config.py # Configuration settings
   │ ├── etl.py # ETL transformation logic
   │ ├── load_postgresql.py # PostgreSQL loader
   │ ├── migrate_to_supabase.py # Supabase migration
   │ ├── query_executor.py # Query execution helper
   │ ├── query_postgresql.py # PostgreSQL query interface
   │ ├── schema_postgresql.sql # Database schema definition
   │ └── test_queries.py # Database tests
   │
   ├── sql_queries/ # Business intelligence queries
   │ ├── sort_patient_by_diagnosis.sql
   │ ├── visits_for_patient.sql
   │ └── visits_per_month.sql
   │
   ├── supabase/ # Supabase-specific files
   │ ├── DIFFERENCES.md # PostgreSQL vs Supabase notes
   │ └── README.md # Supabase setup guide
   │
   └── .pytest_cache/ # Pytest cache (auto-generated)

## Setup Instructions

1. **Clone the repository** (or create the project directory manually):
   ```sh
   git clone <repository-url>
   cd TEST-DATA-ENGINEERING-PROJECT


## Set up virtual environement

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


## install dependencies

pip install -r requirements.txt

## Airlfow Setup

# Create airflow directory if it doesn't exist
mkdir -p ~/airflow

# Set the AIRFLOW_HOME environment variable
export AIRFLOW_HOME=~/airflow

# Initialize the database
airflow db init

# Create a user (admin credentials)
airflow users create \
    --username admin \
    --firstname Admin \
    --firstname User \
    --role Admin \
    --email admin@example.com \
    --password admin

# lunch airlfow
airlfow webserver -p 8080
airflow scheduler 


## Code running

python scripts/query_executor.py


## Output

output/cleaned_patient_data.csv
output/sort_pation_by_diagnosis.csv