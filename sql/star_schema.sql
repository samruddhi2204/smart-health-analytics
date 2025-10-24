-- Example minimal star schema for an analytics warehouse
CREATE TABLE dim_patient (
  patient_key INT PRIMARY KEY,
  sex VARCHAR(20),
  age_group VARCHAR(20)
);

CREATE TABLE dim_date (
  date_key INT PRIMARY KEY,
  date DATE,
  month INT,
  year INT
);

CREATE TABLE fact_visit (
  visit_key INT PRIMARY KEY,
  patient_key INT,
  date_key INT,
  systolic_bp INT,
  diastolic_bp INT,
  glucose_mg_dL INT,
  diagnosis VARCHAR(40)
);
