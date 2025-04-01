SELECT DISTINCT p.*, diagnosis
FROM patients p
JOIN visits v ON p.patient_id = v.patient_id
WHERE v.diagnosis = 'Depression';