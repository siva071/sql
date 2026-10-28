"""Repository functionality check."""
from repositories.employee_repository import employee_repository
from repositories.reporting_repository import reporting_repository

print('='*60)
print('REPOSITORY FUNCTIONALITY CHECK')
print('='*60)

# Test employee repository
print()
print('EMPLOYEE REPOSITORY:')
try:
    employees = employee_repository.get_all_employees()
    print(f'  [OK] get_all_employees: {len(employees)} employees')
except Exception as e:
    print(f'  [ERROR] get_all_employees: {e}')

try:
    emp = employee_repository.get_employee_by_id(1)
    if emp:
        print(f'  [OK] get_employee_by_id: Found {emp["first_name"]}')
    else:
        print(f'  [OK] get_employee_by_id: No employee found')
except Exception as e:
    print(f'  [ERROR] get_employee_by_id: {e}')

try:
    depts = reporting_repository.get_all_departments()
    print(f'  [OK] get_all_departments: {len(depts)} departments')
except Exception as e:
    print(f'  [ERROR] get_all_departments: {e}')

# Test reporting repository
print()
print('REPORTING REPOSITORY:')
try:
    stats = reporting_repository.get_dashboard_stats()
    print(f'  [OK] get_dashboard_stats: {stats["total_employees"]} employees, {stats["total_departments"]} depts')
except Exception as e:
    print(f'  [ERROR] get_dashboard_stats: {e}')

try:
    dept_counts = reporting_repository.get_department_counts()
    print(f'  [OK] get_department_counts: {len(dept_counts)} departments')
except Exception as e:
    print(f'  [ERROR] get_department_counts: {e}')

try:
    salary_stats = reporting_repository.get_department_salary_stats()
    print(f'  [OK] get_department_salary_stats: {len(salary_stats)} departments')
except Exception as e:
    print(f'  [ERROR] get_department_salary_stats: {e}')

try:
    high_earners = reporting_repository.get_employees_above_dept_avg()
    print(f'  [OK] get_employees_above_dept_avg: {len(high_earners)} employees')
except Exception as e:
    print(f'  [ERROR] get_employees_above_dept_avg: {e}')

try:
    trends = reporting_repository.get_hiring_trends()
    print(f'  [OK] get_hiring_trends: {len(trends)} years')
except Exception as e:
    print(f'  [ERROR] get_hiring_trends: {e}')

print()
print('='*60)
print('ALL REPOSITORY CHECKS COMPLETED')
print('='*60)
