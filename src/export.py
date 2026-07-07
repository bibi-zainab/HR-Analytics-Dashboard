"""Utilities for exporting analysis summaries and SQL-ready outputs."""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def build_summary_table(df: pd.DataFrame) -> pd.DataFrame:
    """Create a concise KPI summary table for reporting."""
    summary = {
        "employee_count": int(df.shape[0]),
        "attrition_rate": round(float(df["attrition"].mean() * 100), 2),
        "avg_monthly_income": round(float(df["monthly_income"].mean()), 2),
        "avg_age": round(float(df["age"].mean()), 2),
        "avg_years_at_company": round(float(df["years_at_company"].mean()), 2),
    }
    return pd.DataFrame([summary])


def export_summary(df: pd.DataFrame, output_path: str | Path) -> None:
    """Export a KPI summary table to CSV."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    build_summary_table(df).to_csv(path, index=False)
    LOGGER.info("Exported KPI summary to %s", path)
