-- Seed sample data for Employee Reporting System (PostgreSQL)
-- This script is idempotent - safe to rerun

-- Insert departments (only if not exists)
INSERT INTO departments (department_name, location)
SELECT 'Engineering', 'Building A'
WHERE NOT EXISTS (SELECT 1 FROM departments WHERE department_name = 'Engineering');

INSERT INTO departments (department_name, location)
SELECT 'Marketing', 'Building B'
WHERE NOT EXISTS (SELECT 1 FROM departments WHERE department_name = 'Marketing');

INSERT INTO departments (department_name, location)
SELECT 'Human Resources', 'Building C'
WHERE NOT EXISTS (SELECT 1 FROM departments WHERE department_name = 'Human Resources');

INSERT INTO departments (department_name, location)
SELECT 'Finance', 'Building A'
WHERE NOT EXISTS (SELECT 1 FROM departments WHERE department_name = 'Finance');

INSERT INTO departments (department_name, location)
SELECT 'Sales', 'Building D'
WHERE NOT EXISTS (SELECT 1 FROM departments WHERE department_name = 'Sales');

INSERT INTO departments (department_name, location)
SELECT 'Operations', 'Building E'
WHERE NOT EXISTS (SELECT 1 FROM departments WHERE department_name = 'Operations');

-- Insert employees (only if not exists)
INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
SELECT 'John', 'Smith', 'john.smith@example.com', 1, 75000.00, '2020-01-15'::DATE
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email = 'john.smith@example.com');

INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
SELECT 'Sarah', 'Johnson', 'sarah.johnson@example.com', 1, 82000.00, '2019-06-20'::DATE
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email = 'sarah.johnson@example.com');

INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
SELECT 'Michael', 'Williams', 'michael.williams@example.com', 1, 95000.00, '2018-03-10'::DATE
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email = 'michael.williams@example.com');

INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
SELECT 'Emily', 'Brown', 'emily.brown@example.com', 2, 65000.00, '2021-02-28'::DATE
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email = 'emily.brown@example.com');

INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
SELECT 'David', 'Jones', 'david.jones@example.com', 2, 58000.00, '2022-05-12'::DATE
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email = 'david.jones@example.com');

INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
SELECT 'Jessica', 'Garcia', 'jessica.garcia@example.com', 3, 70000.00, '2020-09-05'::DATE
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email = 'jessica.garcia@example.com');

INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
SELECT 'Robert', 'Miller', 'robert.miller@example.com', 3, 72000.00, '2019-11-18'::DATE
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email = 'robert.miller@example.com');

INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
SELECT 'Amanda', 'Davis', 'amanda.davis@example.com', 4, 85000.00, '2018-07-22'::DATE
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email = 'amanda.davis@example.com');

INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
SELECT 'Christopher', 'Rodriguez', 'christopher.rodriguez@example.com', 4, 90000.00, '2017-04-15'::DATE
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email = 'christopher.rodriguez@example.com');

INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
SELECT 'Michelle', 'Martinez', 'michelle.martinez@example.com', 5, 60000.00, '2021-08-30'::DATE
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email = 'michelle.martinez@example.com');

INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
SELECT 'Daniel', 'Hernandez', 'daniel.hernandez@example.com', 5, 55000.00, '2022-01-10'::DATE
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email = 'daniel.hernandez@example.com');

INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
SELECT 'Laura', 'Lopez', 'laura.lopez@example.com', 5, 62000.00, '2020-12-05'::DATE
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email = 'laura.lopez@example.com');

INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
SELECT 'James', 'Gonzalez', 'james.gonzalez@example.com', 6, 58000.00, '2021-04-20'::DATE
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email = 'james.gonzalez@example.com');

INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
SELECT 'Jennifer', 'Wilson', 'jennifer.wilson@example.com', 6, 61000.00, '2020-07-15'::DATE
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email = 'jennifer.wilson@example.com');

INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
SELECT 'Thomas', 'Anderson', 'thomas.anderson@example.com', 1, 88000.00, '2019-02-25'::DATE
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email = 'thomas.anderson@example.com');

INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
SELECT 'Lisa', 'Thomas', 'lisa.thomas@example.com', 1, 78000.00, '2020-10-12'::DATE
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email = 'lisa.thomas@example.com');

INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
SELECT 'Kevin', 'Taylor', 'kevin.taylor@example.com', 2, 62000.00, '2021-06-08'::DATE
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email = 'kevin.taylor@example.com');

INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
SELECT 'Nancy', 'Moore', 'nancy.moore@example.com', 3, 68000.00, '2020-03-18'::DATE
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email = 'nancy.moore@example.com');

INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
SELECT 'Paul', 'Jackson', 'paul.jackson@example.com', 4, 82000.00, '2018-11-30'::DATE
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email = 'paul.jackson@example.com');

INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
SELECT 'Karen', 'White', 'karen.white@example.com', 5, 57000.00, '2022-03-22'::DATE
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE email = 'karen.white@example.com');
