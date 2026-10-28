"""Input validation utilities for employee data."""
import re
from typing import Tuple, Optional


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate email format.

    Args:
        email: Email address to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"

    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False, "Invalid email format"

    return True, None


def validate_salary(salary: float) -> Tuple[bool, Optional[str]]:
    """
    Validate salary value.

    Args:
        salary: Salary to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if salary is None:
        return False, "Salary is required"

    try:
        salary_float = float(salary)
    except (ValueError, TypeError):
        return False, "Salary must be a number"

    if salary_float <= 0:
        return False, "Salary must be greater than 0"

    if salary_float > 10000000:
        return False, "Salary seems unrealistically high"

    return True, None


def validate_name(name: str, field_name: str = "Name") -> Tuple[bool, Optional[str]]:
    """
    Validate name field.

    Args:
        name: Name to validate
        field_name: Name of the field for error message

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or not name.strip():
        return False, f"{field_name} is required"

    if len(name.strip()) < 2:
        return False, f"{field_name} must be at least 2 characters"

    if len(name) > 50:
        return False, f"{field_name} must be less than 50 characters"

    return True, None


def validate_department_id(department_id: int) -> Tuple[bool, Optional[str]]:
    """
    Validate department ID.

    Args:
        department_id: Department ID to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if department_id is None:
        return False, "Department is required"

    try:
        dept_id = int(department_id)
    except (ValueError, TypeError):
        return False, "Department ID must be a number"

    if dept_id <= 0:
        return False, "Department ID must be positive"

    return True, None


def validate_employee_form(
    first_name: str,
    last_name: str,
    email: str,
    department_id: int,
    salary: float
) -> Tuple[bool, dict]:
    """
    Validate complete employee form.

    Args:
        first_name: Employee first name
        last_name: Employee last name
        email: Employee email
        department_id: Department ID
        salary: Employee salary

    Returns:
        Tuple of (is_valid, errors_dict)
    """
    errors = {}

    is_valid, error = validate_name(first_name, "First name")
    if not is_valid:
        errors['first_name'] = error

    is_valid, error = validate_name(last_name, "Last name")
    if not is_valid:
        errors['last_name'] = error

    is_valid, error = validate_email(email)
    if not is_valid:
        errors['email'] = error

    is_valid, error = validate_department_id(department_id)
    if not is_valid:
        errors['department_id'] = error

    is_valid, error = validate_salary(salary)
    if not is_valid:
        errors['salary'] = error

    return len(errors) == 0, errors
