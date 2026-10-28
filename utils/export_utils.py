"""Export utilities for generating CSV and Excel reports."""
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any


def export_to_csv(data: List[Dict[str, Any]], filename_prefix: str = "report") -> str:
    """
    Export data to CSV file.

    Args:
        data: List of dictionaries containing the data
        filename_prefix: Prefix for the filename

    Returns:
        Path to the generated CSV file
    """
    if not data:
        raise ValueError("No data to export")

    df = pd.DataFrame(data)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.csv"
    filepath = f"reports/{filename}"

    df.to_csv(filepath, index=False)
    return filepath


def export_to_excel(data: List[Dict[str, Any]], filename_prefix: str = "report") -> str:
    """
    Export data to Excel file.

    Args:
        data: List of dictionaries containing the data
        filename_prefix: Prefix for the filename

    Returns:
        Path to the generated Excel file
    """
    if not data:
        raise ValueError("No data to export")

    df = pd.DataFrame(data)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.xlsx"
    filepath = f"reports/{filename}"

    df.to_excel(filepath, index=False, engine='openpyxl')
    return filepath


def format_employee_data_for_export(employees: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Format employee data for export (clean up column names, format dates).

    Args:
        employees: Raw employee data from database

    Returns:
        Formatted employee data
    """
    formatted = []
    for emp in employees:
        formatted_emp = {
            'Employee ID': emp.get('employee_id'),
            'First Name': emp.get('first_name'),
            'Last Name': emp.get('last_name'),
            'Email': emp.get('email'),
            'Department': emp.get('department_name'),
            'Salary': emp.get('salary'),
            'Hire Date': emp.get('hire_date')
        }
        formatted.append(formatted_emp)
    return formatted


def format_department_summary_for_export(departments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Format department summary data for export.

    Args:
        departments: Raw department data from database

    Returns:
        Formatted department summary data
    """
    formatted = []
    for dept in departments:
        formatted_dept = {
            'Department': dept.get('department_name'),
            'Location': dept.get('location'),
            'Employee Count': dept.get('employee_count', 0),
            'Average Salary': dept.get('avg_salary', 0),
            'Minimum Salary': dept.get('min_salary', 0),
            'Maximum Salary': dept.get('max_salary', 0),
            'Total Payroll': dept.get('total_payroll', 0)
        }
        formatted.append(formatted_dept)
    return formatted
