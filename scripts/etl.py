import pandas as pd

# Load each CSV file
demographics          = pd.read_csv('/Users/alaelaroussi/Documents/Work/test_data_engineer/data/patient_demographics.csv')
lab_results           = pd.read_csv('/Users/alaelaroussi/Documents/Work/test_data_engineer/data/patient_lab_results.csv')
medications           = pd.read_csv('/Users/alaelaroussi/Documents/Work/test_data_engineer/data/patient_medications.csv')
visits                = pd.read_csv('/Users/alaelaroussi/Documents/Work/test_data_engineer/data/patient_visits.csv')
physician_assignments = pd.read_csv('/Users/alaelaroussi/Documents/Work/test_data_engineer/data/physician_assignments.csv')

# Rename columns
demographics = demographics.rename(columns={'other_fields': 'maladie_description'})
visits       = visits.rename(columns={'other_fields': 'visit_description'})

medications = medications.rename(columns={'notes': 'medication_notes'})
lab_results = lab_results.rename(columns={'notes': 'lab_notes'})

# Handling missing values
# Fill int missing values with median
demographics['age']         = demographics['age'].fillna(demographics['age'].median())
lab_results['result_value'] = lab_results['result_value'].fillna(lab_results['result_value'].median())


# Fill text missing values
demographics['gender']              = demographics['gender'].fillna('Unknown')
demographics['maladie_description'] = demographics['maladie_description'].fillna('Unknown')
lab_results['lab_notes']            = lab_results['lab_notes'].fillna('Unknown')
medications['medication_notes']     = medications['medication_notes'].fillna('Unknown')
visits['medication']                = visits['medication'].fillna('Unknown')
visits['visit_description']         = visits['visit_description'].fillna('Unknown')
visits['diagnosis']                 = visits['diagnosis'].fillna('Unknown')

# Remove duplicated values
demographics          = demographics.drop_duplicates()
lab_results           = lab_results.drop_duplicates()
medications           = medications.drop_duplicates()
visits                = visits.drop_duplicates()
physician_assignments = physician_assignments.drop_duplicates()

# Change data format
demographics['patient_id'] = demographics['patient_id'].astype(str)
demographics['gender']     = demographics['gender'].astype(str)


lab_results['test_date'] = pd.to_datetime(lab_results['test_date'])

medications['end_date']   = pd.to_datetime(medications['end_date'])
medications['start_date'] = pd.to_datetime(medications['start_date'])

visits['visit_date'] = pd.to_datetime(visits['visit_date'])

physician_assignments['assignment_date'] = pd.to_datetime(physician_assignments['assignment_date'])


# Merge dataframes
# Merge the dataframes on 'patient_id' and 'visit_id'
merged_data = pd.merge(
    visits, 
    demographics, 
    on='patient_id', 
    how='left'
)

merged_data = pd.merge(
    merged_data, 
    medications, 
    on=['patient_id', 'visit_id'], 
    how='left'
)

merged_data = pd.merge(
    merged_data, 
    physician_assignments, 
    on=['patient_id', 'visit_id'], 
    how='left'
)

merged_data = pd.merge(
    merged_data, 
    lab_results, 
    on=['patient_id', 'visit_id'], 
    how='left'
)

# Keep medication details from the medications dataframe
if 'medication_x' in merged_data.columns and 'medication_y' in merged_data.columns:
    merged_data['medication'] = merged_data['medication_y'].fillna(merged_data['medication_x'])
    merged_data.drop(['medication_x', 'medication_y'], axis=1, inplace=True)

# Create new derived fields
visit_counts = merged_data.groupby('patient_id')['visit_id'].count().reset_index()
visit_counts = visit_counts.rename(columns={'visit_id': 'visit_frequency'})
visit_counts['visit_frequency'] = visit_counts['visit_frequency'].astype(int)

merged_data = pd.merge(
    merged_data,
    visit_counts,
    on='patient_id',
    how='left'
)

# Classify patients based on age (age groups)
bins = [0, 18, 30, 50, 120]  # Age ranges
labels = ['<18', '18-30', '31-50', '50+']  # Group names

merged_data['age_group'] = pd.cut(
    merged_data['age'],
    bins=bins,
    labels=labels,
    right=False  # Ensures 30 falls in "18-30", not "31-50"
)

# Save the cleaned and merged data to a new CSV file
merged_data.to_csv('/Users/alaelaroussi/Documents/Work/test_data_engineer/output/cleaned_patient_data.csv', index=False)
