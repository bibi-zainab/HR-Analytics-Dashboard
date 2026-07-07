"""Exploratory data analysis and visualization utilities for the HR analytics project."""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def create_visuals(df: pd.DataFrame, output_dir: str | Path) -> None:
    """Generate a professional set of charts for the HR dashboard."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    sns.set_theme(style="whitegrid")

    charts = {
        "attrition_rate": lambda: plot_attrition_rate(df),
        "department_attrition": lambda: plot_department_attrition(df),
        "job_role_attrition": lambda: plot_job_role_attrition(df),
        "gender_distribution": lambda: plot_gender_distribution(df),
        "salary_distribution": lambda: plot_salary_distribution(df),
        "age_distribution": lambda: plot_age_distribution(df),
        "overtime_analysis": lambda: plot_overtime_analysis(df),
        "job_satisfaction": lambda: plot_job_satisfaction(df),
        "work_life_balance": lambda: plot_work_life_balance(df),
        "years_at_company": lambda: plot_years_at_company(df),
        "monthly_income": lambda: plot_monthly_income(df),
        "correlation_matrix": lambda: plot_correlation_matrix(df),
    }

    for name, plot_fn in charts.items():
        try:
            fig = plot_fn()
            fig.savefig(output_path / f"{name}.png", dpi=300, bbox_inches="tight")
            plt.close(fig)
            LOGGER.info("Saved chart: %s", name)
        except Exception as exc:
            LOGGER.exception("Failed to generate chart %s: %s", name, exc)


def plot_attrition_rate(df: pd.DataFrame) -> plt.Figure:
    """Plot overall employee attrition rate."""
    rate = df["attrition"].mean() * 100
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(["Attrition Rate"], [rate], color="#d9534f")
    ax.set_title("Overall Attrition Rate")
    ax.set_ylabel("Percentage")
    ax.set_ylim(0, 100)
    return fig


def plot_department_attrition(df: pd.DataFrame) -> plt.Figure:
    """Plot attrition rate by department."""
    summary = df.groupby("department")["attrition"].mean().sort_values(ascending=False) * 100
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=summary.index, y=summary.values, palette="coolwarm", ax=ax)
    ax.set_title("Attrition Rate by Department")
    ax.set_ylabel("Attrition %")
    ax.tick_params(axis="x", rotation=45)
    return fig


def plot_job_role_attrition(df: pd.DataFrame) -> plt.Figure:
    """Plot attrition rate by job role."""
    summary = df.groupby("job_role")["attrition"].mean().sort_values(ascending=False) * 100
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=summary.values, y=summary.index, palette="viridis", ax=ax)
    ax.set_title("Attrition Rate by Job Role")
    ax.set_xlabel("Attrition %")
    return fig


def plot_gender_distribution(df: pd.DataFrame) -> plt.Figure:
    """Plot employee distribution by gender."""
    fig, ax = plt.subplots(figsize=(6, 4))
    df["gender"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax, startangle=90)
    ax.set_title("Gender Distribution")
    ax.set_ylabel("")
    return fig


def plot_salary_distribution(df: pd.DataFrame) -> plt.Figure:
    """Plot salary distribution."""
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df["monthly_income"], kde=True, bins=20, color="#4C78A8", ax=ax)
    ax.set_title("Monthly Income Distribution")
    ax.set_xlabel("Monthly Income")
    return fig


def plot_age_distribution(df: pd.DataFrame) -> plt.Figure:
    """Plot age distribution."""
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df["age"], kde=True, bins=20, color="#F58518", ax=ax)
    ax.set_title("Age Distribution")
    ax.set_xlabel("Age")
    return fig


def plot_overtime_analysis(df: pd.DataFrame) -> plt.Figure:
    """Plot attrition by overtime status."""
    summary = df.groupby("overtime")["attrition"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=summary, x="overtime", y="attrition", palette=["#4C78A8", "#F58518"], ax=ax)
    ax.set_title("Attrition by Overtime")
    ax.set_xlabel("Overtime")
    ax.set_ylabel("Attrition Rate")
    return fig


def plot_job_satisfaction(df: pd.DataFrame) -> plt.Figure:
    """Plot job satisfaction distribution."""
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.countplot(data=df, x="job_satisfaction", palette="Set2", ax=ax)
    ax.set_title("Job Satisfaction")
    ax.set_xlabel("Satisfaction Level")
    return fig


def plot_work_life_balance(df: pd.DataFrame) -> plt.Figure:
    """Plot work-life balance distribution."""
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.countplot(data=df, x="work_life_balance", palette="pastel", ax=ax)
    ax.set_title("Work-Life Balance")
    ax.set_xlabel("Balance Level")
    return fig


def plot_years_at_company(df: pd.DataFrame) -> plt.Figure:
    """Plot tenure distribution."""
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df["years_at_company"], kde=True, bins=20, color="#54A24B", ax=ax)
    ax.set_title("Years at Company")
    ax.set_xlabel("Years")
    return fig


def plot_monthly_income(df: pd.DataFrame) -> plt.Figure:
    """Plot monthly income by department."""
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.boxplot(data=df, x="department", y="monthly_income", palette="Blues", ax=ax)
    ax.set_title("Monthly Income by Department")
    ax.set_xlabel("Department")
    ax.set_ylabel("Monthly Income")
    ax.tick_params(axis="x", rotation=45)
    return fig


def plot_correlation_matrix(df: pd.DataFrame) -> plt.Figure:
    """Plot correlation matrix for selected numeric fields."""
    numeric = df.select_dtypes(include="number")
    corr = numeric.corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, cmap="coolwarm", annot=False, ax=ax)
    ax.set_title("Correlation Matrix")
    return fig
