"""Tests for employee service module."""
import pytest
from unittest.mock import Mock, patch
from services.employee_service import employee_service


class TestEmployeeService:
    """Test employee service business logic."""

    @patch('services.employee_service.employee_repository')
    def test_get_all_employees(self, mock_repo):
        """Test getting all employees."""
        mock_repo.get_all_employees.return_value = [
            {'employee_id': 1, 'first_name': 'John', 'last_name': 'Doe'}
        ]

        employees = employee_service.get_all_employees()

        assert len(employees) == 1
        assert employees[0]['first_name'] == 'John'
        mock_repo.get_all_employees.assert_called_once()

    @patch('services.employee_service.employee_repository')
    def test_search_employees_with_term(self, mock_repo):
        """Test searching employees with a search term."""
        mock_repo.search_employees.return_value = [
            {'employee_id': 1, 'first_name': 'John', 'last_name': 'Doe'}
        ]

        employees = employee_service.search_employees("John")

        assert len(employees) == 1
        mock_repo.search_employees.assert_called_once_with("John")

    @patch('services.employee_service.employee_repository')
    def test_search_employees_empty_term(self, mock_repo):
        """Test searching employees with empty term returns all."""
        mock_repo.get_all_employees.return_value = [
            {'employee_id': 1, 'first_name': 'John', 'last_name': 'Doe'}
        ]

        employees = employee_service.search_employees("")

        assert len(employees) == 1
        mock_repo.get_all_employees.assert_called_once()
        mock_repo.search_employees.assert_not_called()

    @patch('services.employee_service.employee_repository')
    def test_create_employee_success(self, mock_repo):
        """Test successful employee creation."""
        mock_repo.create_employee.return_value = 100
        mock_repo.get_employee_by_id.return_value = None

        result = employee_service.create_employee(
            "John", "Doe", "john@example.com", 1, 50000.00, "2024-01-01"
        )

        assert result['success'] is True
        assert 'employee_id' in result
        assert result['employee_id'] == 100

    @patch('services.employee_service.employee_repository')
    def test_create_employee_validation_error(self, mock_repo):
        """Test employee creation with validation error."""
        result = employee_service.create_employee(
            "", "Doe", "john@example.com", 1, 50000.00, "2024-01-01"
        )

        assert result['success'] is False
        assert 'errors' in result
        assert 'first_name' in result['errors']

    @patch('services.employee_service.employee_repository')
    def test_create_employee_duplicate_email(self, mock_repo):
        """Test employee creation with duplicate email."""
        mock_repo.create_employee.side_effect = Exception("Email already exists")

        result = employee_service.create_employee(
            "John", "Doe", "john@example.com", 1, 50000.00, "2024-01-01"
        )

        assert result['success'] is False
        assert 'Email already exists' in result['message']

    @patch('services.employee_service.employee_repository')
    def test_update_employee_success(self, mock_repo):
        """Test successful employee update."""
        mock_repo.get_employee_by_id.return_value = {
            'employee_id': 1, 'first_name': 'John', 'last_name': 'Doe'
        }
        mock_repo.update_employee.return_value = True

        result = employee_service.update_employee(
            1, "Jane", "Doe", "jane@example.com", 1, 60000.00
        )

        assert result['success'] is True

    @patch('services.employee_service.employee_repository')
    def test_update_employee_not_found(self, mock_repo):
        """Test updating non-existent employee."""
        mock_repo.get_employee_by_id.return_value = None

        result = employee_service.update_employee(
            999, "Jane", "Doe", "jane@example.com", 1, 60000.00
        )

        assert result['success'] is False
        assert 'not found' in result['message']

    @patch('services.employee_service.employee_repository')
    def test_delete_employee_success(self, mock_repo):
        """Test successful employee deletion."""
        mock_repo.get_employee_by_id.return_value = {
            'employee_id': 1, 'first_name': 'John', 'last_name': 'Doe'
        }
        mock_repo.delete_employee.return_value = True

        result = employee_service.delete_employee(1)

        assert result['success'] is True

    @patch('services.employee_service.employee_repository')
    def test_delete_employee_not_found(self, mock_repo):
        """Test deleting non-existent employee."""
        mock_repo.get_employee_by_id.return_value = None

        result = employee_service.delete_employee(999)

        assert result['success'] is False
        assert 'not found' in result['message']
