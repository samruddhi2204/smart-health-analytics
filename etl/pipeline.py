from __future__ import annotations
import pandas as pd
from pathlib import Path
from . import qc

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CURATED = DATA_DIR / "curated"
CURATED.mkdir(exist_ok=True, parents=True)

RAW = DATA_DIR / "raw_patients.csv"
REPORT = CURATED / "dq_report.html"

PII_COLS = [c for c in ["name","email","phone","address"] if c in []]  # placeholder

def deidentify(df: pd.DataFrame) -> pd.DataFrame:
    # No PII in the sample, but keep hook for future
    return df.copy()

def run_qc(df: pd.DataFrame) -> pd.DataFrame:
    checks = [
        qc.check_non_negative(df, "age"),
        qc.check_in_range(df, "age", 0, 120),
        qc.check_missing(df, "weight_kg"),
        qc.check_in_range(df, "glucose_mg_dL", 40, 600),
        qc.zscore_flags(df, "systolic_bp"),
        qc.zscore_flags(df, "diastolic_bp"),
    ]
    summary = qc.summarize(checks)
    return summary

def save_report(summary: pd.DataFrame):
    html = summary.to_html(index=False)
    REPORT.write_text("""<h2>Data Quality Report</h2>""" + html)

def main():
    df = pd.read_csv(RAW, parse_dates=["last_visit"])
    qc_summary = run_qc(df)
    save_report(qc_summary)

    # Basic cleaning rules
    df = df[df["age"] >= 0]
    df.loc[df["glucose_mg_dL"] > 600, "glucose_mg_dL"] = None
    df = deidentify(df)

    # Save curated datasets
    df.to_parquet(CURATED / "patients.parquet", index=False)
    df.to_csv(CURATED / "patients.csv", index=False)
    print("ETL complete. Curated files written to:", CURATED)
    print("QC summary:\n", qc_summary)

if __name__ == "__main__":
    main()
