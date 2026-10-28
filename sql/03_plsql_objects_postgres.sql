-- PostgreSQL Stored Functions and Procedures
-- These are PostgreSQL equivalents of the Oracle PL/SQL objects
-- Run this after the tables are created

-- ============================================================================
-- 1. Function: Calculate Department Average Salary
-- Equivalent to Oracle: fn_dept_avg_salary
-- ============================================================================

CREATE OR REPLACE FUNCTION fn_dept_avg_salary(p_department_id INTEGER)
RETURNS NUMERIC AS $$
BEGIN
    RETURN (
        SELECT ROUND(AVG(salary), 2)
        FROM employees
        WHERE department_id = p_department_id
    );
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 2. Function: Get Employee Count by Department
-- Equivalent to Oracle: fn_employee_count
-- ============================================================================

CREATE OR REPLACE FUNCTION fn_employee_count(p_department_id INTEGER)
RETURNS INTEGER AS $$
BEGIN
    RETURN (
        SELECT COUNT(*)
        FROM employees
        WHERE department_id = p_department_id
    );
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 3. Function: Insert Employee with Validation
-- Equivalent to Oracle: sp_insert_employee (converted to function returning JSON)
-- PostgreSQL doesn't have OUT parameters like Oracle, so we return a JSON object
-- ============================================================================

CREATE OR REPLACE FUNCTION sp_insert_employee(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_email VARCHAR,
    p_department_id INTEGER,
    p_salary NUMERIC,
    p_hire_date DATE
)
RETURNS JSON AS $$
DECLARE
    v_email_count INTEGER;
    v_dept_count INTEGER;
    v_employee_id INTEGER;
    v_result JSON;
BEGIN
    -- Validate email uniqueness
    SELECT COUNT(*) INTO v_email_count
    FROM employees
    WHERE email = p_email;

    IF v_email_count > 0 THEN
        RETURN json_build_object(
            'success', false,
            'message', 'Email already exists',
            'employee_id', NULL::INTEGER
        );
    END IF;

    -- Validate department exists
    SELECT COUNT(*) INTO v_dept_count
    FROM departments
    WHERE department_id = p_department_id;

    IF v_dept_count = 0 THEN
        RETURN json_build_object(
            'success', false,
            'message', 'Department does not exist',
            'employee_id', NULL::INTEGER
        );
    END IF;

    -- Validate salary
    IF p_salary <= 0 THEN
        RETURN json_build_object(
            'success', false,
            'message', 'Salary must be positive',
            'employee_id', NULL::INTEGER
        );
    END IF;

    -- Insert employee
    INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
    VALUES (p_first_name, p_last_name, p_email, p_department_id, p_salary, p_hire_date)
    RETURNING employee_id INTO v_employee_id;

    RETURN json_build_object(
        'success', true,
        'message', 'Employee inserted successfully',
        'employee_id', v_employee_id
    );

EXCEPTION
    WHEN OTHERS THEN
        RETURN json_build_object(
            'success', false,
            'message', 'Database error: ' || SQLERRM,
            'employee_id', NULL::INTEGER
        );
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 4. Function: Update Employee Salary with Validation
-- Equivalent to Oracle: sp_update_employee_salary (converted to function)
-- ============================================================================

CREATE OR REPLACE FUNCTION sp_update_employee_salary(
    p_employee_id INTEGER,
    p_new_salary NUMERIC
)
RETURNS JSON AS $$
DECLARE
    v_emp_count INTEGER;
BEGIN
    -- Validate employee exists
    SELECT COUNT(*) INTO v_emp_count
    FROM employees
    WHERE employee_id = p_employee_id;

    IF v_emp_count = 0 THEN
        RETURN json_build_object(
            'success', false,
            'message', 'Employee does not exist'
        );
    END IF;

    -- Validate salary
    IF p_new_salary <= 0 THEN
        RETURN json_build_object(
            'success', false,
            'message', 'Salary must be positive'
        );
    END IF;

    -- Update salary
    UPDATE employees
    SET salary = p_new_salary
    WHERE employee_id = p_employee_id;

    RETURN json_build_object(
        'success', true,
        'message', 'Salary updated successfully'
    );

EXCEPTION
    WHEN OTHERS THEN
        RETURN json_build_object(
            'success', false,
            'message', 'Database error: ' || SQLERRM
        );
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 5. Function: Department-wise Report
-- Equivalent to Oracle: sp_department_report (converted to function returning SETOF)
-- ============================================================================

CREATE OR REPLACE FUNCTION sp_department_report(p_department_id INTEGER DEFAULT NULL)
RETURNS TABLE (
    department_name VARCHAR,
    location VARCHAR,
    employee_count BIGINT,
    avg_salary NUMERIC,
    min_salary NUMERIC,
    max_salary NUMERIC,
    total_payroll NUMERIC
) AS $$
BEGIN
    IF p_department_id IS NULL THEN
        -- Report for all departments
        RETURN QUERY
        SELECT
            d.department_name,
            d.location,
            COUNT(e.employee_id) AS employee_count,
            ROUND(AVG(e.salary), 2) AS avg_salary,
            MIN(e.salary) AS min_salary,
            MAX(e.salary) AS max_salary,
            ROUND(SUM(e.salary), 2) AS total_payroll
        FROM departments d
        LEFT JOIN employees e ON d.department_id = e.department_id
        GROUP BY d.department_name, d.location
        ORDER BY d.department_name;
    ELSE
        -- Report for specific department
        RETURN QUERY
        SELECT
            d.department_name,
            d.location,
            COUNT(e.employee_id) AS employee_count,
            ROUND(AVG(e.salary), 2) AS avg_salary,
            MIN(e.salary) AS min_salary,
            MAX(e.salary) AS max_salary,
            ROUND(SUM(e.salary), 2) AS total_payroll
        FROM departments d
        LEFT JOIN employees e ON d.department_id = e.department_id
        WHERE d.department_id = p_department_id
        GROUP BY d.department_name, d.location;
    END IF;
END;
$$ LANGUAGE plpgsql;
