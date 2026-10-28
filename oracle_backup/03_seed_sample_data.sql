-- Seed sample data for Employee Reporting System
-- WARNING: This script checks for existing data to avoid duplicates
-- Safe to rerun if data already exists

-- Insert departments
DECLARE
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count FROM departments;
    IF v_count = 0 THEN
        INSERT INTO departments (department_name, location) VALUES
        ('Engineering', 'Building A'),
        ('Marketing', 'Building B'),
        ('Human Resources', 'Building C'),
        ('Finance', 'Building A'),
        ('Sales', 'Building D'),
        ('Operations', 'Building E');
        COMMIT;
        DBMS_OUTPUT.PUT_LINE('Departments seeded successfully');
    ELSE
        DBMS_OUTPUT.PUT_LINE('Departments already exist, skipping');
    END IF;
END;
/

-- Insert employees
DECLARE
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count FROM employees;
    IF v_count = 0 THEN
        INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date) VALUES
        ('John', 'Smith', 'john.smith@example.com', 1, 75000.00, TO_DATE('2020-01-15', 'YYYY-MM-DD')),
        ('Sarah', 'Johnson', 'sarah.johnson@example.com', 1, 82000.00, TO_DATE('2019-06-20', 'YYYY-MM-DD')),
        ('Michael', 'Williams', 'michael.williams@example.com', 1, 95000.00, TO_DATE('2018-03-10', 'YYYY-MM-DD')),
        ('Emily', 'Brown', 'emily.brown@example.com', 2, 65000.00, TO_DATE('2021-02-28', 'YYYY-MM-DD')),
        ('David', 'Jones', 'david.jones@example.com', 2, 58000.00, TO_DATE('2022-05-12', 'YYYY-MM-DD')),
        ('Jessica', 'Garcia', 'jessica.garcia@example.com', 3, 70000.00, TO_DATE('2020-09-05', 'YYYY-MM-DD')),
        ('Robert', 'Miller', 'robert.miller@example.com', 3, 72000.00, TO_DATE('2019-11-18', 'YYYY-MM-DD')),
        ('Amanda', 'Davis', 'amanda.davis@example.com', 4, 85000.00, TO_DATE('2018-07-22', 'YYYY-MM-DD')),
        ('Christopher', 'Rodriguez', 'christopher.rodriguez@example.com', 4, 90000.00, TO_DATE('2017-04-15', 'YYYY-MM-DD')),
        ('Michelle', 'Martinez', 'michelle.martinez@example.com', 5, 60000.00, TO_DATE('2021-08-30', 'YYYY-MM-DD')),
        ('Daniel', 'Hernandez', 'daniel.hernandez@example.com', 5, 55000.00, TO_DATE('2022-01-10', 'YYYY-MM-DD')),
        ('Laura', 'Lopez', 'laura.lopez@example.com', 5, 62000.00, TO_DATE('2020-12-05', 'YYYY-MM-DD')),
        ('James', 'Gonzalez', 'james.gonzalez@example.com', 6, 58000.00, TO_DATE('2021-04-20', 'YYYY-MM-DD')),
        ('Jennifer', 'Wilson', 'jennifer.wilson@example.com', 6, 61000.00, TO_DATE('2020-07-15', 'YYYY-MM-DD')),
        ('Thomas', 'Anderson', 'thomas.anderson@example.com', 1, 88000.00, TO_DATE('2019-02-25', 'YYYY-MM-DD')),
        ('Lisa', 'Thomas', 'lisa.thomas@example.com', 1, 78000.00, TO_DATE('2020-10-12', 'YYYY-MM-DD')),
        ('Kevin', 'Taylor', 'kevin.taylor@example.com', 2, 62000.00, TO_DATE('2021-06-08', 'YYYY-MM-DD')),
        ('Nancy', 'Moore', 'nancy.moore@example.com', 3, 68000.00, TO_DATE('2020-03-18', 'YYYY-MM-DD')),
        ('Paul', 'Jackson', 'paul.jackson@example.com', 4, 82000.00, TO_DATE('2018-11-30', 'YYYY-MM-DD')),
        ('Karen', 'White', 'karen.white@example.com', 5, 57000.00, TO_DATE('2022-03-22', 'YYYY-MM-DD'));
        COMMIT;
        DBMS_OUTPUT.PUT_LINE('Employees seeded successfully');
    ELSE
        DBMS_OUTPUT.PUT_LINE('Employees already exist, skipping');
    END IF;
END;
/

-- Verify data
SELECT 'Total Departments: ' || COUNT(*) FROM departments;
SELECT 'Total Employees: ' || COUNT(*) FROM employees;
