"""Data loading and cleaning utilities for the HR Analytics Dashboard project."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import pandas as pd

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def load_raw_data(file_path: str | Path) -> pd.DataFrame:
    """Load the raw employee attrition CSV into a pandas DataFrame."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Raw dataset not found: {path}")

    try:
        df = pd.read_csv(path)
        LOGGER.info("Loaded raw data with %s rows and %s columns", df.shape[0], df.shape[1])
        return df
    except Exception as exc:
        LOGGER.exception("Failed to load raw dataset from %s", path)
        raise RuntimeError(f"Unable to read dataset: {exc}") from exc


def clean_employee_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the HR dataset by removing duplicates, handling missing values, and typing columns."""
    cleaned = df.copy()

    cleaned = cleaned.drop_duplicates()

    for col in ["Attrition", "BusinessTravel", "Department", "EducationField", "Gender", "JobRole", "MaritalStatus", "OverTime"]:
        if col in cleaned.columns:
            cleaned[col] = cleaned[col].astype("string")

    for col in ["Age", "DailyRate", "DistanceFromHome", "Education", "EmployeeCount", "EmployeeNumber", "EnvironmentSatisfaction", "HourlyRate", "JobInvolvement", "JobLevel", "JobSatisfaction", "MonthlyIncome", "MonthlyRate", "NumCompaniesWorked", "PercentSalaryHike", "PerformanceRating", "RelationshipSatisfaction", "StandardHours", "StockOptionLevel", "TotalWorkingYears", "TrainingTimesLastYear", "WorkLifeBalance", "YearsAtCompany", "YearsInCurrentRole", "YearsSinceLastPromotion", "YearsWithCurrManager"]:
        if col in cleaned.columns:
            cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    cleaned["Attrition"] = cleaned["Attrition"].map({"Yes": 1, "No": 0}).astype("Int64")
    cleaned["OverTime"] = cleaned["OverTime"].map({"Yes": 1, "No": 0}).astype("Int64")

    cleaned = cleaned.rename(columns={
        "Age": "age",
        "Attrition": "attrition",
        "BusinessTravel": "business_travel",
        "DailyRate": "daily_rate",
        "Department": "department",
        "DistanceFromHome": "distance_from_home",
        "Education": "education",
        "EducationField": "education_field",
        "EmployeeCount": "employee_count",
        "EmployeeNumber": "employee_number",
        "EnvironmentSatisfaction": "environment_satisfaction",
        "Gender": "gender",
        "HourlyRate": "hourly_rate",
        "JobInvolvement": "job_involvement",
        "JobLevel": "job_level",
        "JobRole": "job_role",
        "JobSatisfaction": "job_satisfaction",
        "MaritalStatus": "marital_status",
        "MonthlyIncome": "monthly_income",
        "MonthlyRate": "monthly_rate",
        "NumCompaniesWorked": "num_companies_worked",
        "Over18": "over_18",
        "OverTime": "overtime",
        "PercentSalaryHike": "percent_salary_hike",
        "PerformanceRating": "performance_rating",
        "RelationshipSatisfaction": "relationship_satisfaction",
        "StandardHours": "standard_hours",
        "StockOptionLevel": "stock_option_level",
        "TotalWorkingYears": "total_working_years",
        "TrainingTimesLastYear": "training_times_last_year",
        "WorkLifeBalance": "work_life_balance",
        "YearsAtCompany": "years_at_company",
        "YearsInCurrentRole": "years_in_current_role",
        "YearsSinceLastPromotion": "years_since_last_promotion",
        "YearsWithCurrManager": "years_with_curr_manager",
    })

    cleaned["income_band"] = pd.cut(
        cleaned["monthly_income"],
        bins=[0, 5000, 10000, 15000, 20000, float("inf")],
        labels=["Low", "Medium", "High", "Very High", "Executive"],
        include_lowest=True,
    )
    cleaned["age_group"] = pd.cut(
        cleaned["age"],
        bins=[0, 25, 35, 45, 55, float("inf")],
        labels=["Under 25", "25-35", "36-45", "46-55", "55+"],
        include_lowest=True,
    )
    cleaned["tenure_band"] = pd.cut(
        cleaned["years_at_company"],
        bins=[0, 2, 5, 10, 15, float("inf")],
        labels=["Early", "Established", "Stable", "Senior", "Veteran"],
        include_lowest=True,
    )

    numeric_cols = cleaned.select_dtypes(include="number").columns
    for col in numeric_cols:
        if col in {"employee_count", "standard_hours"}:
            continue
        q1 = cleaned[col].quantile(0.25)
        q3 = cleaned[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        cleaned[col] = cleaned[col].clip(lower=lower, upper=upper)

    cleaned = cleaned.dropna(subset=["department", "job_role", "gender"])

    LOGGER.info("Cleaned dataset shape: %s", cleaned.shape)
    return cleaned


def save_processed_data(df: pd.DataFrame, output_path: str | Path) -> None:
    """Save the cleaned dataset to disk for downstream analysis and reporting."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    LOGGER.info("Saved processed data to %s", path)
