-- Enable Row Level Security (RLS) for Supabase
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
ALTER TABLE physicians ENABLE ROW LEVEL SECURITY;
ALTER TABLE visits ENABLE ROW LEVEL SECURITY;
ALTER TABLE medications ENABLE ROW LEVEL SECURITY;
ALTER TABLE lab_results ENABLE ROW LEVEL SECURITY;



-- PATIENTS TABLE
CREATE TABLE patients (
    patient_id VARCHAR(10) PRIMARY KEY,
    age FLOAT,
    gender VARCHAR(20),
    maladie_description TEXT,
    visit_frequency INTEGER,
    age_group VARCHAR(10)
);

-- PHYSICIANS TABLE
CREATE TABLE physicians (
    physician_id VARCHAR(10) PRIMARY KEY,
    physician_name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL
);

-- VISITS TABLE
CREATE TABLE visits (
    visit_id VARCHAR(10) PRIMARY KEY,
    patient_id VARCHAR(10) REFERENCES patients(patient_id),
    visit_date DATE NOT NULL,
    diagnosis TEXT,
    visit_description TEXT,
    physician_id VARCHAR(10) REFERENCES physicians(physician_id),
    assignment_date DATE,
    medication TEXT
);

-- MEDICATIONS TABLE
CREATE TABLE medications (
    medication_id VARCHAR(10) PRIMARY KEY,
    patient_id VARCHAR(10) REFERENCES patients(patient_id),
    visit_id VARCHAR(10) REFERENCES visits(visit_id),
    medication VARCHAR(100),
    dosage VARCHAR(20),
    start_date DATE,
    end_date DATE,
    medication_notes TEXT
);

-- LAB RESULTS TABLE
CREATE TABLE lab_results (
    lab_test_id VARCHAR(10) PRIMARY KEY,
    patient_id VARCHAR(10) REFERENCES patients(patient_id),
    visit_id VARCHAR(10) REFERENCES visits(visit_id),
    test_date DATE,
    test_name VARCHAR(100),
    result_value FLOAT,
    result_unit VARCHAR(20),
    reference_range VARCHAR(50),
    lab_notes TEXT
);

-- INDEXES FOR PERFORMANCE
CREATE INDEX idx_patient_visits ON visits(patient_id);
CREATE INDEX idx_visit_meds ON medications(visit_id);

