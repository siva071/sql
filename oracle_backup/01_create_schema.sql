-- Create database schema for Employee Reporting System
-- Run this script as the application user (hr_app)

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;

-- Create departments table
CREATE TABLE departments (
    department_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    department_name VARCHAR2(50) NOT NULL UNIQUE,
    location VARCHAR2(100)
);

-- Create employees table
CREATE TABLE employees (
    employee_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR2(50) NOT NULL,
    last_name VARCHAR2(50) NOT NULL,
    email VARCHAR2(100) NOT NULL UNIQUE,
    department_id NUMBER NOT NULL,
    salary NUMBER(10, 2) NOT NULL CHECK (salary > 0),
    hire_date DATE NOT NULL,
    CONSTRAINT fk_department
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);

-- Create indexes for performance
CREATE INDEX idx_employees_department ON employees(department_id);
CREATE INDEX idx_employees_hire_date ON employees(hire_date);
CREATE INDEX idx_employees_salary ON employees(salary);

COMMIT;
