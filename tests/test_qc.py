import pandas as pd
from etl.pipeline import run_qc
import pathlib

def test_qc_has_rules():
    df = pd.read_csv(pathlib.Path(__file__).parents[1] / 'data' / 'raw_patients.csv')
    summary = run_qc(df)
    assert len(summary) >= 1
    assert {'rule','checked_rows','failed_rows','fail_rate_pct'} <= set(summary.columns)
