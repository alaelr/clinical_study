# Patient Data ETL Pipeline

This project is a simple ETL (Extract, Transform, Load) pipeline for processing patient-related data. It reads multiple CSV files, cleans and transforms the data, and merges them into a final dataset.

## Project Structure

TEST - DATA ENGINEERING PROJECT/
│── data/                      # Raw CSV data files
│   ├── patient_demographics.csv
│   ├── patient_lab_results.csv
│   ├── patient_medications.csv
│   ├── patient_visits.csv
│   ├── physician_assignments.csv
│── output/                    # Processed output files
│── scripts/                   # Python scripts
│   ├── database.py
│   ├── etl.py                 # Main ETL script
│── venv/                      # Virtual environment (if used)
│── README.md                  # Documentation
│── requirements.txt            # Python dependencies


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


## Code running

python scripts/etl.py


## Output

output/cleaned_patient_data.csv