# Patient Data ETL Pipeline

This project is a simple ETL (Extract, Transform, Load) pipeline for processing patient-related data. It reads multiple CSV files, cleans and transforms the data, and merges them into a final dataset.


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

### Create airflow directory if it doesn't exist
mkdir -p ~/airflow

### Set the AIRFLOW_HOME environment variable
export AIRFLOW_HOME=~/airflow

### Initialize the database
airflow db init

### Create a user (admin credentials)
airflow users create \
    --username admin \
    --firstname Admin \
    --firstname User \
    --role Admin \
    --email admin@example.com \
    --password admin

### lunch airlfow
airlfow webserver -p 8080
airflow scheduler 


## Code running

python scripts/query_executor.py


## Output

output/cleaned_patient_data.csv
output/sort_pation_by_diagnosis.csv