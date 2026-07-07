# HR Analytics Dashboard

## Project Overview
This project builds a production-quality HR analytics portfolio using the IBM HR Analytics Employee Attrition dataset. The goal is to transform raw employee data into a clean, insightful, and presentation-ready analysis workflow with Python, SQL, and Power BI.

## Business Problem
Organizations need to understand employee turnover patterns, identify departments with higher attrition risk, and evaluate factors such as salary, overtime, job satisfaction, and tenure. This project addresses those needs by combining data cleaning, exploratory analysis, SQL reporting, and dashboarding.

## Dataset Information
- Source: IBM HR Analytics Employee Attrition dataset
- Rows: 1,470
- Columns: 35
- Key dimensions: department, job role, gender, overtime, age, income, tenure, satisfaction, workload balance, and attrition

## Technologies Used
- Python 3.12
- Pandas
- NumPy
- Matplotlib
- Seaborn
- MySQL
- Power BI
- Excel
- Git and GitHub

## Folder Structure
```text
HR-Analytics-Dashboard/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── EDA.ipynb
├── src/
│   ├── data_cleaning.py
│   ├── eda.py
│   └── export.py
├── sql/
│   └── hr_queries.sql
├── dashboard/
│   └── HR_Dashboard.pbix
├── images/
├── reports/
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation Steps
1. Clone the repository.
2. Create a virtual environment.
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Place the raw CSV file in the data/raw folder.
5. Run the main pipeline:
   ```bash
   python src/run_pipeline.py
   ```

## Key Insights
- Attrition is often concentrated in specific departments and job roles.
- Overtime and lower job satisfaction are associated with higher attrition risk.
- Salary bands and tenure have strong influence on employee retention.
- Demographics such as age and gender can highlight workforce trends.

## Dashboard Preview Placeholder
A Power BI dashboard file is included in the dashboard folder for portfolio presentation.

## Future Improvements
- Add a forecasting module for attrition prediction.
- Connect the dashboard to a live SQL database.
- Automate the ETL workflow with scheduled pipelines.
- Expand analysis with employee engagement metrics.
