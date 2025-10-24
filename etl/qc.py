from __future__ import annotations
import pandas as pd
import numpy as np

class QCResult(pd.DataFrame):
    """A lightweight result object carrying rule-level outcomes."""
    @property
    def _constructor(self):
        return QCResult

def check_non_negative(df: pd.DataFrame, col: str) -> QCResult:
    failing = df[df[col] < 0]
    return QCResult({
        "rule": [f"{col} >= 0"],
        "checked_rows": [len(df)],
        "failed_rows": [len(failing)],
    })

def check_in_range(df: pd.DataFrame, col: str, low: float, high: float) -> QCResult:
    failing = df[(df[col] < low) | (df[col] > high) | df[col].isna()]
    return QCResult({
        "rule": [f"{col} in [{low}, {high}]"],
        "checked_rows": [len(df)],
        "failed_rows": [len(failing)],
    })

def check_missing(df: pd.DataFrame, col: str) -> QCResult:
    missing = df[col].isna().sum()
    return QCResult({
        "rule": [f"{col} not null"],
        "checked_rows": [len(df)],
        "failed_rows": [int(missing)],
    })

def zscore_flags(df: pd.DataFrame, col: str, threshold: float = 3.5) -> QCResult:
    x = df[col].astype(float)
    mu, sigma = x.mean(), x.std(ddof=0)
    if sigma == 0 or np.isnan(sigma):
        fails = 0
    else:
        z = (x - mu) / sigma
        fails = int((z.abs() > threshold).sum())
    return QCResult({
        "rule": [f"{col} |z| <= {threshold}"],
        "checked_rows": [len(df)],
        "failed_rows": [fails],
    })

def summarize(results: list[QCResult]) -> pd.DataFrame:
    out = pd.concat(results, ignore_index=True)
    out["fail_rate_pct"] = (out["failed_rows"] / out["checked_rows"]).round(4) * 100
    return out
