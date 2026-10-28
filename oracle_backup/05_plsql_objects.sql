-- PL/SQL Stored Procedures and Functions
-- This script creates optional PL/SQL objects for the Employee Reporting System
-- Run this after the tables are created

-- ============================================================================
-- 1. Stored Procedure: Insert Employee with Validation
-- ============================================================================

CREATE OR REPLACE PROCEDURE sp_insert_employee(
    p_first_name IN VARCHAR2,
    p_last_name IN VARCHAR2,
    p_email IN VARCHAR2,
    p_department_id IN NUMBER,
    p_salary IN NUMBER,
    p_hire_date IN DATE,
    p_employee_id OUT NUMBER,
    p_status OUT VARCHAR2,
    p_message OUT VARCHAR2
)
AS
    v_email_count NUMBER;
    v_dept_count NUMBER;
BEGIN
    -- Validate email uniqueness
    SELECT COUNT(*) INTO v_email_count
    FROM employees
    WHERE email = p_email;

    IF v_email_count > 0 THEN
        p_status := 'ERROR';
        p_message := 'Email already exists';
        p_employee_id := NULL;
        RETURN;
    END IF;

    -- Validate department exists
    SELECT COUNT(*) INTO v_dept_count
    FROM departments
    WHERE department_id = p_department_id;

    IF v_dept_count = 0 THEN
        p_status := 'ERROR';
        p_message := 'Department does not exist';
        p_employee_id := NULL;
        RETURN;
    END IF;

    -- Validate salary
    IF p_salary <= 0 THEN
        p_status := 'ERROR';
        p_message := 'Salary must be positive';
        p_employee_id := NULL;
        RETURN;
    END IF;

    -- Insert employee
    INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
    VALUES (p_first_name, p_last_name, p_email, p_department_id, p_salary, p_hire_date)
    RETURNING employee_id INTO p_employee_id;

    COMMIT;
    p_status := 'SUCCESS';
    p_message := 'Employee inserted successfully';

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Database error: ' || SQLERRM;
        p_employee_id := NULL;
END sp_insert_employee;
/

-- ============================================================================
-- 2. Function: Calculate Department Average Salary
-- ============================================================================

CREATE OR REPLACE FUNCTION fn_dept_avg_salary(p_department_id IN NUMBER)
RETURN NUMBER
AS
    v_avg_salary NUMBER;
BEGIN
    SELECT AVG(salary) INTO v_avg_salary
    FROM employees
    WHERE department_id = p_department_id;

    RETURN ROUND(v_avg_salary, 2);

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN 0;
    WHEN OTHERS THEN
        RETURN NULL;
END fn_dept_avg_salary;
/

-- ============================================================================
-- 3. Stored Procedure: Department-wise Report
-- ============================================================================

CREATE OR REPLACE PROCEDURE sp_department_report(
    p_department_id IN NUMBER DEFAULT NULL,
    p_cursor OUT SYS_REFCURSOR
)
AS
BEGIN
    IF p_department_id IS NULL THEN
        -- Report for all departments
        OPEN p_cursor FOR
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
        OPEN p_cursor FOR
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
EXCEPTION
    WHEN OTHERS THEN
        RAISE;
END sp_department_report;
/

-- ============================================================================
-- 4. Function: Get Employee Count by Department
-- ============================================================================

CREATE OR REPLACE FUNCTION fn_employee_count(p_department_id IN NUMBER)
RETURN NUMBER
AS
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM employees
    WHERE department_id = p_department_id;

    RETURN v_count;

EXCEPTION
    WHEN OTHERS THEN
        RETURN 0;
END fn_employee_count;
/

-- ============================================================================
-- 5. Stored Procedure: Update Employee Salary with Validation
-- ============================================================================

CREATE OR REPLACE PROCEDURE sp_update_employee_salary(
    p_employee_id IN NUMBER,
    p_new_salary IN NUMBER,
    p_status OUT VARCHAR2,
    p_message OUT VARCHAR2
)
AS
    v_emp_count NUMBER;
BEGIN
    -- Validate employee exists
    SELECT COUNT(*) INTO v_emp_count
    FROM employees
    WHERE employee_id = p_employee_id;

    IF v_emp_count = 0 THEN
        p_status := 'ERROR';
        p_message := 'Employee does not exist';
        RETURN;
    END IF;

    -- Validate salary
    IF p_new_salary <= 0 THEN
        p_status := 'ERROR';
        p_message := 'Salary must be positive';
        RETURN;
    END IF;

    -- Update salary
    UPDATE employees
    SET salary = p_new_salary
    WHERE employee_id = p_employee_id;

    COMMIT;
    p_status := 'SUCCESS';
    p_message := 'Salary updated successfully';

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        p_status := 'ERROR';
        p_message := 'Database error: ' || SQLERRM;
END sp_update_employee_salary;
/

-- ============================================================================
-- Testing the PL/SQL Objects
-- ============================================================================

-- Test the function
-- SELECT fn_dept_avg_salary(1) FROM dual;

-- Test the procedure (uncomment to test)
-- DECLARE
--     v_emp_id NUMBER;
--     v_status VARCHAR2(50);
--     v_message VARCHAR2(200);
-- BEGIN
--     sp_insert_employee(
--         'Test', 'User', 'test.user@example.com',
--         1, 65000, SYSDATE,
--         v_emp_id, v_status, v_message
--     );
--     DBMS_OUTPUT.PUT_LINE('Status: ' || v_status || ', Message: ' || v_message);
--     DBMS_OUTPUT.PUT_LINE('Employee ID: ' || v_emp_id);
-- END;
-- /

COMMIT;
