-- Create database schema for Employee Reporting System (PostgreSQL)
-- Run this script as the application user

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS departments CASCADE;

-- Create departments table
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(50) NOT NULL UNIQUE,
    location VARCHAR(100)
);

-- Create employees table
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    department_id INTEGER NOT NULL,
    salary NUMERIC(10, 2) NOT NULL CHECK (salary > 0),
    hire_date DATE NOT NULL,
    CONSTRAINT fk_department
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);

-- Create indexes for performance
CREATE INDEX idx_employees_department ON employees(department_id);
CREATE INDEX idx_employees_hire_date ON employees(hire_date);
CREATE INDEX idx_employees_salary ON employees(salary);
