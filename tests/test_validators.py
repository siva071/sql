"""Tests for validators module."""
import pytest
from utils.validators import (
    validate_email,
    validate_salary,
    validate_name,
    validate_department_id,
    validate_employee_form
)


class TestEmailValidation:
    """Test email validation."""

    def test_valid_email(self):
        """Test valid email format."""
        is_valid, error = validate_email("test@example.com")
        assert is_valid is True
        assert error is None

    def test_invalid_email_format(self):
        """Test invalid email format."""
        is_valid, error = validate_email("invalid-email")
        assert is_valid is False
        assert error == "Invalid email format"

    def test_empty_email(self):
        """Test empty email."""
        is_valid, error = validate_email("")
        assert is_valid is False
        assert error == "Email is required"

    def test_none_email(self):
        """Test None email."""
        is_valid, error = validate_email(None)
        assert is_valid is False
        assert error == "Email is required"


class TestSalaryValidation:
    """Test salary validation."""

    def test_valid_salary(self):
        """Test valid salary."""
        is_valid, error = validate_salary(50000.00)
        assert is_valid is True
        assert error is None

    def test_zero_salary(self):
        """Test zero salary (invalid)."""
        is_valid, error = validate_salary(0)
        assert is_valid is False
        assert error == "Salary must be greater than 0"

    def test_negative_salary(self):
        """Test negative salary (invalid)."""
        is_valid, error = validate_salary(-1000)
        assert is_valid is False
        assert error == "Salary must be greater than 0"

    def test_none_salary(self):
        """Test None salary."""
        is_valid, error = validate_salary(None)
        assert is_valid is False
        assert error == "Salary is required"

    def test_string_salary(self):
        """Test string salary (should fail)."""
        is_valid, error = validate_salary("not a number")
        assert is_valid is False
        assert error == "Salary must be a number"

    def test_unrealistically_high_salary(self):
        """Test unrealistically high salary."""
        is_valid, error = validate_salary(20000000)
        assert is_valid is False
        assert error == "Salary seems unrealistically high"


class TestNameValidation:
    """Test name validation."""

    def test_valid_name(self):
        """Test valid name."""
        is_valid, error = validate_name("John")
        assert is_valid is True
        assert error is None

    def test_empty_name(self):
        """Test empty name."""
        is_valid, error = validate_name("")
        assert is_valid is False
        assert error == "Name is required"

    def test_whitespace_name(self):
        """Test whitespace-only name."""
        is_valid, error = validate_name("   ")
        assert is_valid is False
        assert error == "Name is required"

    def test_short_name(self):
        """Test name that's too short."""
        is_valid, error = validate_name("J")
        assert is_valid is False
        assert error == "Name must be at least 2 characters"

    def test_long_name(self):
        """Test name that's too long."""
        is_valid, error = validate_name("A" * 51)
        assert is_valid is False
        assert error == "Name must be less than 50 characters"


class TestDepartmentIdValidation:
    """Test department ID validation."""

    def test_valid_department_id(self):
        """Test valid department ID."""
        is_valid, error = validate_department_id(1)
        assert is_valid is True
        assert error is None

    def test_zero_department_id(self):
        """Test zero department ID (invalid)."""
        is_valid, error = validate_department_id(0)
        assert is_valid is False
        assert error == "Department ID must be positive"

    def test_negative_department_id(self):
        """Test negative department ID (invalid)."""
        is_valid, error = validate_department_id(-1)
        assert is_valid is False
        assert error == "Department ID must be positive"

    def test_none_department_id(self):
        """Test None department ID."""
        is_valid, error = validate_department_id(None)
        assert is_valid is False
        assert error == "Department is required"


class TestEmployeeFormValidation:
    """Test complete employee form validation."""

    def test_valid_form(self):
        """Test completely valid form."""
        is_valid, errors = validate_employee_form(
            "John", "Doe", "john@example.com", 1, 50000.00
        )
        assert is_valid is True
        assert len(errors) == 0

    def test_invalid_email(self):
        """Test form with invalid email."""
        is_valid, errors = validate_employee_form(
            "John", "Doe", "invalid-email", 1, 50000.00
        )
        assert is_valid is False
        assert 'email' in errors

    def test_invalid_salary(self):
        """Test form with invalid salary."""
        is_valid, errors = validate_employee_form(
            "John", "Doe", "john@example.com", 1, -1000
        )
        assert is_valid is False
        assert 'salary' in errors

    def test_multiple_errors(self):
        """Test form with multiple validation errors."""
        is_valid, errors = validate_employee_form(
            "", "Doe", "invalid", 0, -1000
        )
        assert is_valid is False
        assert len(errors) > 1
        assert 'first_name' in errors
        assert 'email' in errors
        assert 'salary' in errors
