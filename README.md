# Smart Health Analytics

ETL + QC + patient-safe analytics for healthcare intelligence.

**Stack:** Python · Pandas · SQL · Azure DevOps · Streamlit

## Quickstart

```bash
# 1) Create a virtual env (optional) and install deps
pip install -r requirements.txt

# 2) Run ETL (cleans + validates + de-identifies)
python -m etl.pipeline

# 3) Launch the Streamlit app
streamlit run app.py
```

The app ships with synthetic sample data in `data/raw_patients.csv`.
Output cleansed data will be written to `data/curated/`.

## Features

- **ETL:** ingest CSV, validate schema, apply data quality checks, and de-identify PHI columns
- **QC:** range checks, null checks, z-score outlier flags, and a compact HTML data quality report
- **Analytics UI:** KPI cards, filterable trends, and simple cohort analysis in Streamlit
- **Security by design:** works only with de-identified data and writes minimal artifacts
- **CI:** Azure DevOps pipeline runs unit tests and style checks on each push

## Repo layout

```
smart-health-analytics/
├─ app.py
├─ requirements.txt
├─ etl/
│  ├─ pipeline.py
│  └─ qc.py
├─ data/
│  └─ raw_patients.csv
├─ sql/
│  └─ star_schema.sql
├─ tests/
│  └─ test_qc.py
└─ azure-pipelines.yml
```

---

© 2025 Smart Health Analytics (sample project)
