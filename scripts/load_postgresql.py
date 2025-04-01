import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def insert_with_conflict_handling(table, data, engine, unique_column):
    """
    Insert data into a table while avoiding duplicates using `ON CONFLICT DO NOTHING`.
    """
    if data.empty:
        print(f"No data to insert into {table}. Skipping...")
        return
    
    with engine.begin() as conn:
        for _, row in data.iterrows():
            try:
                columns = ", ".join(data.columns)
                values_placeholders = ", ".join([f":{col}" for col in data.columns])
                
                sql_query = f"""
                INSERT INTO {table} ({columns}) 
                VALUES ({values_placeholders})
                ON CONFLICT ({unique_column}) DO NOTHING;
                """
                
                conn.execute(text(sql_query), row.to_dict())

            except SQLAlchemyError as e:
                print(f" Error inserting into {table}: {str(e)}")

def load_data():
    # Load cleaned data
    df = pd.read_csv('/Users/alaelaroussi/Documents/Work/test_data_engineer/output/cleaned_patient_data.csv')

    # Create database connection
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/clinical_study')

    try:
        # Disable foreign key checks temporarily
        with engine.begin() as conn:
            conn.execute(text("SET session_replication_role = 'replica';"))
        
        print("Foreign key constraints disabled")

        # Prepare data
        tables = {
            'patients': df[['patient_id', 'age', 'gender', 'maladie_description', 
                            'visit_frequency', 'age_group']].drop_duplicates('patient_id'),
            
            'physicians': df[['physician_id', 'physician_name', 'department']]
                          .drop_duplicates('physician_id'),
            
            'visits': df[['visit_id', 'patient_id', 'visit_date', 'diagnosis',
                          'visit_description', 'physician_id', 'assignment_date', 'medication']]
                     .drop_duplicates('visit_id'),
            
            'medications': df[['medication_id', 'patient_id', 'visit_id', 'medication',
                               'dosage', 'start_date', 'end_date', 'medication_notes']]
                          .dropna(subset=['medication_id'])
                          .drop_duplicates('medication_id'),
            
            'lab_results': df[['lab_test_id', 'patient_id', 'visit_id', 'test_date',
                               'test_name', 'result_value', 'result_unit', 
                               'reference_range', 'lab_notes']]
                          .dropna(subset=['lab_test_id'])
                          .drop_duplicates('lab_test_id')
        }

        # Load data in dependency order with conflict handling
        insert_with_conflict_handling("patients", tables["patients"], engine, "patient_id")
        insert_with_conflict_handling("physicians", tables["physicians"], engine, "physician_id")
        insert_with_conflict_handling("visits", tables["visits"], engine, "visit_id")
        insert_with_conflict_handling("medications", tables["medications"], engine, "medication_id")
        insert_with_conflict_handling("lab_results", tables["lab_results"], engine, "lab_test_id")

        print(" Data successfully loaded into all tables!")

    except SQLAlchemyError as e:
        print(f" Error loading data: {e}")

    finally:
        # Re-enable foreign key checks
        with engine.begin() as conn:
            conn.execute(text("SET session_replication_role = 'origin';"))
        print(" Foreign key constraints re-enabled")

if __name__ == "__main__":
    load_data()
    print(" Data loading complete!")