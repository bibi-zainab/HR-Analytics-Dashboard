import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pandas as pd

from data_cleaning import clean_employee_data, load_raw_data


class DataCleaningTests(unittest.TestCase):
    def test_clean_employee_data_renames_columns_and_creates_bands(self) -> None:
        raw_path = Path(__file__).resolve().parents[1] / "data" / "raw" / "employee_attrition.csv"
        self.assertTrue(raw_path.exists(), "Raw dataset should exist before running tests")

        df = load_raw_data(raw_path)
        cleaned = clean_employee_data(df)

        self.assertIn("age", cleaned.columns)
        self.assertIn("attrition", cleaned.columns)
        self.assertIn("income_band", cleaned.columns)
        self.assertIn("age_group", cleaned.columns)
        self.assertIn("tenure_band", cleaned.columns)
        self.assertGreaterEqual(len(cleaned), 1)


if __name__ == "__main__":
    unittest.main()
