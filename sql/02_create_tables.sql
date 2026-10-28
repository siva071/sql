-- Additional database objects and views
-- This script is optional - 01_create_schema.sql creates the core tables

-- Create a view for employee summary with department names
CREATE OR REPLACE VIEW v_employee_summary AS
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    e.email,
    d.department_name,
    e.salary,
    e.hire_date
FROM employees e
JOIN departments d ON e.department_id = d.department_id;

-- Create a sequence for manual employee ID generation if needed
-- Note: Oracle 12c+ uses IDENTITY columns, but sequence can be useful
CREATE SEQUENCE seq_employee_id
    START WITH 1000
    INCREMENT BY 1
    NOCACHE;

COMMIT;
