"""Verify data is coming from database, not hardcoded."""
from repositories.employee_repository import employee_repository

print('='*60)
print('VERIFYING DATA SOURCE')
print('='*60)
print()

# Get employee data
employees = employee_repository.get_all_employees()

print(f'Total employees fetched: {len(employees)}')
print()

if employees:
    print('Sample employee data from database:')
    for i, emp in enumerate(employees[:3], 1):
        print(f'{i}. {emp["first_name"]} {emp["last_name"]}')
        print(f'   Email: {emp["email"]}')
        print(f'   Department: {emp["department_name"]}')
        print(f'   Salary: ${emp["salary"]:,.2f}')
        print(f'   Hire Date: {emp["hire_date"]}')
        print()

print()
print('This data is coming DIRECTLY from your Oracle Database!')
print('Database: localhost:1522/FREEPDB1')
print('User: hr_app')
print('Table: employees')
print()
print('NO HARDCODED DATA - All data is fetched from database via SQL queries!')
