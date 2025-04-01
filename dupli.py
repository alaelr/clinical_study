import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def load_data():
    # Load cleaned data
    df = pd.read_csv('/Users/alaelaroussi/Documents/Work/test_data_engineer/output/cleaned_patient_data.csv')

    # Create database connection
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/clinical_study')

    try:
        # Disable foreign key checks temporarily
        with engine.begin() as conn:
            conn.execute(text("SET session_replication_role = 'replica';"))

        # Prepare tables data in correct load order
        tables = {
            'patients': df[['patient_id', 'age', 'gender', 'maladie_description', 
                          'visit_frequency', 'age_group']].drop_duplicates('patient_id'),
            
            'physicians': df[['physician_id', 'physician_name', 'department']]
                        .drop_duplicates('physician_id'),
            
            'visits': df[['visit_id', 'patient_id', 'visit_date', 'diagnosis',
                         'visit_description', 'physician_id', 'assignment_date', 'medication']],
            
            'medications': df[['medication_id', 'patient_id', 'visit_id', 'medication',
                             'dosage', 'start_date', 'end_date', 'medication_notes']]
                          .dropna(subset=['medication_id']),
            
            'lab_results': df[['lab_test_id', 'patient_id', 'visit_id', 'test_date',
                             'test_name', 'result_value', 'result_unit', 
                             'reference_range', 'lab_notes']]
                          .dropna(subset=['lab_test_id'])
        }

        # Load data in dependency order
        for table in ['patients', 'physicians', 'visits', 'medications', 'lab_results']:
            data = tables[table]
            data.to_sql(
                name=table,
                con=engine,
                if_exists='append',
                index=False,
                method='multi'
            )
            print(f"Successfully loaded {len(data)} rows into {table}")

    except SQLAlchemyError as e:
        print(f"Error loading data: {e}")
    finally:
        # Re-enable foreign key checks
        with engine.begin() as conn:
            conn.execute(text("SET session_replication_role = 'origin';"))
        print("Foreign key constraints re-enabled")

if __name__ == "__main__":
    load_data()
    print("Data loading complete!")