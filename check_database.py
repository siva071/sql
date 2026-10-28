"""Database verification script."""
import oracledb
from config.settings import settings

print('='*60)
print('DATABASE CONNECTION CHECK')
print('='*60)
print(f'Host: {settings.DB_HOST}')
print(f'Port: {settings.DB_PORT}')
print(f'Service: {settings.DB_SERVICE}')
print(f'User: {settings.DB_USER}')
print()

try:
    conn = oracledb.connect(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        dsn=settings.connection_string
    )
    print('[OK] Database connection successful!')
    print()

    cursor = conn.cursor()

    # Check tables
    print('='*60)
    print('TABLES CHECK')
    print('='*60)
    cursor.execute("SELECT table_name FROM user_tables ORDER BY table_name")
    tables = cursor.fetchall()
    print(f'Tables found: {len(tables)}')
    for table in tables:
        print(f'  - {table[0]}')
    print()

    # Check departments
    print('='*60)
    print('DEPARTMENTS DATA CHECK')
    print('='*60)
    cursor.execute('SELECT COUNT(*) FROM departments')
    dept_count = cursor.fetchone()[0]
    print(f'Departments: {dept_count}')
    if dept_count > 0:
        cursor.execute('SELECT department_id, department_name FROM departments ORDER BY department_id')
        depts = cursor.fetchall()
        for dept in depts:
            print(f'  ID {dept[0]}: {dept[1]}')
    print()

    # Check employees
    print('='*60)
    print('EMPLOYEES DATA CHECK')
    print('='*60)
    cursor.execute('SELECT COUNT(*) FROM employees')
    emp_count = cursor.fetchone()[0]
    print(f'Employees: {emp_count}')
    if emp_count > 0:
        cursor.execute('SELECT employee_id, first_name, last_name, department_id FROM employees ORDER BY employee_id')
        emps = cursor.fetchall()
        print('Sample employees:')
        for emp in emps[:5]:
            print(f'  ID {emp[0]}: {emp[1]} {emp[2]} (Dept: {emp[3]})')
        if len(emps) > 5:
            print(f'  ... and {len(emps) - 5} more')
    print()

    # Check PL/SQL objects
    print('='*60)
    print('PL/SQL OBJECTS CHECK')
    print('='*60)
    cursor.execute("SELECT object_name, object_type FROM user_objects WHERE object_type IN ('PROCEDURE', 'FUNCTION') ORDER BY object_type, object_name")
    plsql_objects = cursor.fetchall()
    print(f'PL/SQL objects found: {len(plsql_objects)}')
    for obj in plsql_objects:
        print(f'  - {obj[1]}: {obj[0]}')
    print()

    cursor.close()
    conn.close()
    print('[OK] All checks completed successfully!')

except Exception as e:
    print(f'[ERROR] {e}')
    import traceback
    traceback.print_exc()
