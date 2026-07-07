-- HR Analytics SQL Queries for IBM HR Employee Attrition Dataset
-- This script contains 25+ business-oriented queries for portfolio use.

USE hr_analytics;

-- 1. Basic employee overview
SELECT COUNT(*) AS total_employees
FROM employees;

-- 2. Attrition count
SELECT COUNT(*) AS attrition_count
FROM employees
WHERE attrition = 1;

-- 3. Attrition rate
SELECT ROUND(AVG(CASE WHEN attrition = 1 THEN 1 ELSE 0 END) * 100, 2) AS attrition_rate_pct
FROM employees;

-- 4. Department-wise attrition
SELECT department, ROUND(AVG(CASE WHEN attrition = 1 THEN 1 ELSE 0 END) * 100, 2) AS attrition_rate_pct
FROM employees
GROUP BY department
ORDER BY attrition_rate_pct DESC;

-- 5. Gender distribution
SELECT gender, COUNT(*) AS employee_count
FROM employees
GROUP BY gender
ORDER BY employee_count DESC;

-- 6. Average salary by department
SELECT department, ROUND(AVG(monthly_income), 2) AS avg_monthly_income
FROM employees
GROUP BY department
ORDER BY avg_monthly_income DESC;

-- 7. Employees with overtime and attrition
SELECT department, COUNT(*) AS employees_with_overtime
FROM employees
WHERE overtime = 1
GROUP BY department
ORDER BY employees_with_overtime DESC;

-- 8. High salary employees leaving the company
SELECT employee_number, department, job_role, monthly_income
FROM employees
WHERE attrition = 1 AND monthly_income > 10000
ORDER BY monthly_income DESC;

-- 9. Job satisfaction distribution
SELECT job_satisfaction, COUNT(*) AS employee_count
FROM employees
GROUP BY job_satisfaction
ORDER BY job_satisfaction;

-- 10. Work-life balance by department
SELECT department, ROUND(AVG(work_life_balance), 2) AS avg_work_life_balance
FROM employees
GROUP BY department
ORDER BY avg_work_life_balance DESC;

-- 11. Employees with high tenure and low salary
SELECT employee_number, department, years_at_company, monthly_income
FROM employees
WHERE years_at_company >= 10 AND monthly_income < 5000
ORDER BY years_at_company DESC;

-- 12. Attrition by age group
SELECT CASE
         WHEN age < 30 THEN 'Under 30'
         WHEN age BETWEEN 30 AND 40 THEN '30-40'
         ELSE '40+'
       END AS age_group,
       COUNT(*) AS employee_count,
       ROUND(AVG(CASE WHEN attrition = 1 THEN 1 ELSE 0 END) * 100, 2) AS attrition_rate_pct
FROM employees
GROUP BY age_group
ORDER BY attrition_rate_pct DESC;

-- 13. Employees in sales department with low satisfaction
SELECT employee_number, job_role, job_satisfaction, monthly_income
FROM employees
WHERE department = 'Sales' AND job_satisfaction <= 2
ORDER BY monthly_income DESC;

-- 14. Count of employees by marital status and attrition
SELECT marital_status, attrition, COUNT(*) AS employee_count
FROM employees
GROUP BY marital_status, attrition
ORDER BY marital_status, attrition;

-- 15. Departments exceeding average income threshold
SELECT department, ROUND(AVG(monthly_income), 2) AS avg_income
FROM employees
GROUP BY department
HAVING AVG(monthly_income) > 7000
ORDER BY avg_income DESC;

-- 16. Top 10 employees by monthly income
SELECT employee_number, department, job_role, monthly_income
FROM employees
ORDER BY monthly_income DESC
LIMIT 10;

-- 17. Employees with highest training and low attrition
SELECT employee_number, department, training_times_last_year, attrition
FROM employees
WHERE training_times_last_year >= 3 AND attrition = 0
ORDER BY training_times_last_year DESC;

-- 18. Attrition by overtime and gender
SELECT overtime, gender, COUNT(*) AS employee_count,
       ROUND(AVG(CASE WHEN attrition = 1 THEN 1 ELSE 0 END) * 100, 2) AS attrition_rate_pct
FROM employees
GROUP BY overtime, gender
ORDER BY overtime, gender;

-- 19. Department with highest average performance rating
SELECT department, ROUND(AVG(performance_rating), 2) AS avg_performance_rating
FROM employees
GROUP BY department
ORDER BY avg_performance_rating DESC
LIMIT 1;

-- 20. Employees who left after 5+ years
SELECT employee_number, department, years_at_company, monthly_income
FROM employees
WHERE attrition = 1 AND years_at_company >= 5
ORDER BY years_at_company DESC;

-- 21. Subquery: employees earning above department average
SELECT employee_number, department, monthly_income
FROM employees e1
WHERE monthly_income > (
    SELECT AVG(monthly_income)
    FROM employees e2
    WHERE e2.department = e1.department
)
ORDER BY monthly_income DESC;

-- 22. Subquery: Departments with attrition above overall average
SELECT department
FROM employees
GROUP BY department
HAVING AVG(CASE WHEN attrition = 1 THEN 1 ELSE 0 END) > (
    SELECT AVG(CASE WHEN attrition = 1 THEN 1 ELSE 0 END)
    FROM employees
)
ORDER BY department;

-- 23. Employee count by job role and department
SELECT job_role, department, COUNT(*) AS employee_count
FROM employees
GROUP BY job_role, department
ORDER BY employee_count DESC;

-- 24. Attrition trend by years at company
SELECT years_at_company, COUNT(*) AS employee_count,
       ROUND(AVG(CASE WHEN attrition = 1 THEN 1 ELSE 0 END) * 100, 2) AS attrition_rate_pct
FROM employees
GROUP BY years_at_company
ORDER BY years_at_company;

-- 25. Employees with low salary and high overtime
SELECT employee_number, department, monthly_income, overtime
FROM employees
WHERE monthly_income < 4000 AND overtime = 1
ORDER BY monthly_income ASC;

-- 26. Average monthly income by age band and gender
SELECT CASE
         WHEN age < 30 THEN 'Under 30'
         WHEN age BETWEEN 30 AND 40 THEN '30-40'
         ELSE '40+'
       END AS age_group,
       gender,
       ROUND(AVG(monthly_income), 2) AS avg_monthly_income
FROM employees
GROUP BY age_group, gender
ORDER BY age_group, gender;

-- 27. Highest attrition job roles in research department
SELECT job_role, COUNT(*) AS employee_count,
       ROUND(AVG(CASE WHEN attrition = 1 THEN 1 ELSE 0 END) * 100, 2) AS attrition_rate_pct
FROM employees
WHERE department = 'Research & Development'
GROUP BY job_role
ORDER BY attrition_rate_pct DESC;

-- 28. Employees with above-average training and salary
SELECT employee_number, department, training_times_last_year, monthly_income
FROM employees
WHERE training_times_last_year > (
    SELECT AVG(training_times_last_year) FROM employees
) AND monthly_income > (
    SELECT AVG(monthly_income) FROM employees
)
ORDER BY monthly_income DESC;
