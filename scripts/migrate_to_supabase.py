import pandas as pd
from sqlalchemy import create_engine

# 1. Connect to Source (PostgreSQL)
source_engine = create_engine('postgresql://postgres:postgres@localhost:5432/clinical_study')

# 2. Connect to Supabase
supabase_url = "postgresql://postgres:postgres@localhost:54322/postgres"
supabase_engine = create_engine(supabase_url)

# 3. Tables to migrate
tables = ['patients', 'physicians', 'visits', 'medications', 'lab_results']

# 4. Migration process
for table in tables:
    # Read from PostgreSQL
    df = pd.read_sql(f"SELECT * FROM {table}", source_engine)
    
    # Write to Supabase
    df.to_sql(
        table,
        supabase_engine,
        if_exists='replace',
        index=False
    )
    print(f"Migrated {len(df)} rows to {table}")

print("Migration complete!")