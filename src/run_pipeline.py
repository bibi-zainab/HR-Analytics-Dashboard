"""End-to-end pipeline for the HR Analytics Dashboard project."""

from __future__ import annotations

import shutil
from pathlib import Path

from data_cleaning import clean_employee_data, load_raw_data, save_processed_data
from eda import create_visuals
from export import export_summary

ROOT = Path(__file__).resolve().parent.parent
RAW_DATA = ROOT / "data" / "raw" / "employee_attrition.csv"
PROCESSED_DATA = ROOT / "data" / "processed" / "employee_attrition_clean.csv"
IMAGES_DIR = ROOT / "images"
REPORTS_DIR = ROOT / "reports"


def main() -> None:
    """Run the complete workflow from raw CSV to cleaned outputs and visuals."""
    if not RAW_DATA.exists():
        raise FileNotFoundError(f"Expected raw dataset at {RAW_DATA}")

    df = load_raw_data(RAW_DATA)
    cleaned = clean_employee_data(df)
    save_processed_data(cleaned, PROCESSED_DATA)
    create_visuals(cleaned, IMAGES_DIR)
    export_summary(cleaned, REPORTS_DIR / "summary.csv")

    print(f"Processed rows: {len(cleaned)}")
    print(f"Cleaned dataset saved to: {PROCESSED_DATA}")
    print(f"Charts saved to: {IMAGES_DIR}")
    print(f"Summary saved to: {REPORTS_DIR / 'summary.csv'}")


if __name__ == "__main__":
    main()
