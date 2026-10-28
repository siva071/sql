-- SQL Reporting Queries for Employee Reporting System
-- This file contains example queries demonstrating SQL concepts
-- These are reference queries, not DDL to be executed

-- ============================================================================
-- 1. Basic SELECT and WHERE
-- ============================================================================

-- Select all employees
SELECT employee_id, first_name, last_name, email, salary, hire_date
FROM employees;

-- Filter by department
SELECT e.employee_id, e.first_name, e.last_name, d.department_name
FROM employees e
JOIN departments d ON e.department_id = d.department_id
WHERE d.department_name = 'Engineering';

-- Filter by salary range
SELECT first_name, last_name, salary
FROM employees
WHERE salary BETWEEN 60000 AND 80000;

-- Search by name
SELECT first_name, last_name, email
FROM employees
WHERE UPPER(first_name) LIKE '%JOHN%' OR UPPER(last_name) LIKE '%JOHN%';

-- ============================================================================
-- 2. ORDER BY
-- ============================================================================

-- Order employees by salary (highest first)
SELECT first_name, last_name, salary
FROM employees
ORDER BY salary DESC;

-- Order by department and then by hire date
SELECT d.department_name, e.first_name, e.last_name, e.hire_date
FROM employees e
JOIN departments d ON e.department_id = d.department_id
ORDER BY d.department_name, e.hire_date DESC;

-- ============================================================================
-- 3. GROUP BY and HAVING
-- ============================================================================

-- Count employees per department
SELECT d.department_name, COUNT(e.employee_id) AS employee_count
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_name
ORDER BY employee_count DESC;

-- Average salary per department
SELECT d.department_name,
       ROUND(AVG(e.salary), 2) AS avg_salary,
       COUNT(e.employee_id) AS employee_count
FROM departments d
JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_name
ORDER BY avg_salary DESC;

-- Departments with more than 3 employees
SELECT d.department_name, COUNT(e.employee_id) AS employee_count
FROM departments d
JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_name
HAVING COUNT(e.employee_id) > 3
ORDER BY employee_count DESC;

-- ============================================================================
-- 4. Aggregate Functions (COUNT, SUM, AVG, MIN, MAX)
-- ============================================================================

-- Overall statistics
SELECT
    COUNT(*) AS total_employees,
    SUM(salary) AS total_salary,
    ROUND(AVG(salary), 2) AS avg_salary,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary
FROM employees;

-- Department-wise salary analysis
SELECT
    d.department_name,
    COUNT(e.employee_id) AS employee_count,
    SUM(e.salary) AS total_salary,
    ROUND(AVG(e.salary), 2) AS avg_salary,
    MIN(e.salary) AS min_salary,
    MAX(e.salary) AS max_salary
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_name
ORDER BY total_salary DESC;

-- ============================================================================
-- 5. INNER JOIN and LEFT JOIN
-- ============================================================================

-- INNER JOIN: Only departments with employees
SELECT d.department_name, COUNT(e.employee_id) AS employee_count
FROM departments d
INNER JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_name;

-- LEFT JOIN: All departments, even those without employees
SELECT d.department_name, COUNT(e.employee_id) AS employee_count
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_name;

-- Full employee details with department information
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    e.email,
    d.department_name,
    d.location,
    e.salary,
    e.hire_date
FROM employees e
INNER JOIN departments d ON e.department_id = d.department_id;

-- ============================================================================
-- 6. Subqueries
-- ============================================================================

-- Employees earning above the overall average salary
SELECT first_name, last_name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
ORDER BY salary DESC;

-- Highest paid employee in each department
SELECT d.department_name, e.first_name, e.last_name, e.salary
FROM employees e
JOIN departments d ON e.department_id = d.department_id
WHERE e.salary = (
    SELECT MAX(e2.salary)
    FROM employees e2
    WHERE e2.department_id = e.department_id
)
ORDER BY d.department_name;

-- Employees hired in the last year
SELECT first_name, last_name, hire_date
FROM employees
WHERE hire_date >= ADD_MONTHS(SYSDATE, -12)
ORDER BY hire_date DESC;

-- ============================================================================
-- 7. Common Table Expressions (CTE)
-- ============================================================================

-- Department-wise average salary and employees above average
WITH dept_avg AS (
    SELECT
        department_id,
        AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department_id
)
SELECT
    d.department_name,
    e.first_name,
    e.last_name,
    e.salary,
    da.avg_salary,
    ROUND(e.salary - da.avg_salary, 2) AS salary_difference
FROM employees e
JOIN departments d ON e.department_id = d.department_id
JOIN dept_avg da ON e.department_id = da.department_id
WHERE e.salary > da.avg_salary
ORDER BY d.department_name, e.salary DESC;

-- Monthly hiring trends
WITH monthly_hires AS (
    SELECT
        TO_CHAR(hire_date, 'YYYY-MM') AS hire_month,
        COUNT(*) AS hires_count
    FROM employees
    GROUP BY TO_CHAR(hire_date, 'YYYY-MM')
)
SELECT hire_month, hires_count
FROM monthly_hires
ORDER BY hire_month;

-- ============================================================================
-- 8. Date-based Reports
-- ============================================================================

-- Employees hired in a specific year
SELECT first_name, last_name, hire_date
FROM employees
WHERE EXTRACT(YEAR FROM hire_date) = 2020
ORDER BY hire_date;

-- Years of service for each employee
SELECT
    first_name,
    last_name,
    hire_date,
    ROUND(MONTHS_BETWEEN(SYSDATE, hire_date) / 12, 1) AS years_of_service
FROM employees
ORDER BY years_of_service DESC;

-- ============================================================================
-- 9. Complex Multi-table Queries
-- ============================================================================

-- Department summary with key metrics
SELECT
    d.department_name,
    d.location,
    COUNT(e.employee_id) AS total_employees,
    ROUND(AVG(e.salary), 2) AS average_salary,
    MIN(e.salary) AS minimum_salary,
    MAX(e.salary) AS maximum_salary,
    ROUND(SUM(e.salary), 2) AS total_payroll
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_name, d.location
ORDER BY total_payroll DESC;

-- Employees with salary above their department average
WITH dept_stats AS (
    SELECT
        department_id,
        AVG(salary) AS dept_avg_salary
    FROM employees
    GROUP BY department_id
)
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    d.department_name,
    e.salary,
    ds.dept_avg_salary,
    ROUND((e.salary / ds.dept_avg_salary - 1) * 100, 1) AS pct_above_avg
FROM employees e
JOIN departments d ON e.department_id = d.department_id
JOIN dept_stats ds ON e.department_id = ds.department_id
WHERE e.salary > ds.dept_avg_salary
ORDER BY pct_above_avg DESC;
