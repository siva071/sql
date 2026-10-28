"""Employee service layer for business logic."""
import logging
from typing import List, Dict, Any, Optional
from repositories.employee_repository import employee_repository
from utils.validators import validate_employee_form, ValidationError

logger = logging.getLogger(__name__)


class EmployeeService:
    """Service layer for employee business logic."""

    def get_all_employees(self) -> List[Dict[str, Any]]:
        """
        Get all employees.

        Returns:
            List of employee dictionaries
        """
        try:
            return employee_repository.get_all_employees()
        except Exception as e:
            logger.error(f"Service error fetching employees: {e}")
            raise

    def get_employee_by_id(self, employee_id: int) -> Optional[Dict[str, Any]]:
        """
        Get employee by ID.

        Args:
            employee_id: Employee ID

        Returns:
            Employee dictionary or None
        """
        try:
            return employee_repository.get_employee_by_id(employee_id)
        except Exception as e:
            logger.error(f"Service error fetching employee {employee_id}: {e}")
            raise

    def search_employees(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search employees by name or ID.

        Args:
            search_term: Search term

        Returns:
            List of matching employee dictionaries
        """
        if not search_term or not search_term.strip():
            return self.get_all_employees()

        try:
            return employee_repository.search_employees(search_term.strip())
        except Exception as e:
            logger.error(f"Service error searching employees: {e}")
            raise

    def filter_employees(
        self,
        department_id: Optional[int] = None,
        min_salary: Optional[float] = None,
        max_salary: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Filter employees by criteria.

        Args:
            department_id: Optional department filter
            min_salary: Optional minimum salary filter
            max_salary: Optional maximum salary filter

        Returns:
            List of filtered employee dictionaries
        """
        try:
            return employee_repository.filter_employees(
                department_id=department_id,
                min_salary=min_salary,
                max_salary=max_salary
            )
        except Exception as e:
            logger.error(f"Service error filtering employees: {e}")
            raise

    def create_employee(
        self,
        first_name: str,
        last_name: str,
        email: str,
        department_id: int,
        salary: float,
        hire_date: str
    ) -> Dict[str, Any]:
        """
        Create a new employee with validation.

        Args:
            first_name: First name
            last_name: Last name
            email: Email
            department_id: Department ID
            salary: Salary
            hire_date: Hire date (YYYY-MM-DD)

        Returns:
            Dictionary with success status and message
        """
        # Validate input
        is_valid, errors = validate_employee_form(
            first_name, last_name, email, department_id, salary
        )

        if not is_valid:
            return {
                'success': False,
                'message': 'Validation failed',
                'errors': errors
            }

        try:
            new_id = employee_repository.create_employee(
                first_name=first_name,
                last_name=last_name,
                email=email,
                department_id=department_id,
                salary=salary,
                hire_date=hire_date
            )

            return {
                'success': True,
                'message': f'Employee created successfully with ID: {new_id}',
                'employee_id': new_id
            }

        except Exception as e:
            error_msg = str(e)
            if 'Email already exists' in error_msg:
                return {
                    'success': False,
                    'message': 'Email already exists in the system',
                    'errors': {'email': 'Email already exists'}
                }
            else:
                logger.error(f"Service error creating employee: {e}")
                return {
                    'success': False,
                    'message': f'Failed to create employee: {error_msg}'
                }

    def update_employee(
        self,
        employee_id: int,
        first_name: str,
        last_name: str,
        email: str,
        department_id: int,
        salary: float
    ) -> Dict[str, Any]:
        """
        Update an existing employee with validation.

        Args:
            employee_id: Employee ID to update
            first_name: First name
            last_name: Last name
            email: Email
            department_id: Department ID
            salary: Salary

        Returns:
            Dictionary with success status and message
        """
        # Validate input
        is_valid, errors = validate_employee_form(
            first_name, last_name, email, department_id, salary
        )

        if not is_valid:
            return {
                'success': False,
                'message': 'Validation failed',
                'errors': errors
            }

        # Check if employee exists
        existing = employee_repository.get_employee_by_id(employee_id)
        if not existing:
            return {
                'success': False,
                'message': f'Employee with ID {employee_id} not found'
            }

        try:
            success = employee_repository.update_employee(
                employee_id=employee_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                department_id=department_id,
                salary=salary
            )

            if success:
                return {
                    'success': True,
                    'message': f'Employee {employee_id} updated successfully'
                }
            else:
                return {
                    'success': False,
                    'message': 'No changes made or employee not found'
                }

        except Exception as e:
            error_msg = str(e)
            if 'Email already exists' in error_msg:
                return {
                    'success': False,
                    'message': 'Email already exists in the system',
                    'errors': {'email': 'Email already exists'}
                }
            else:
                logger.error(f"Service error updating employee: {e}")
                return {
                    'success': False,
                    'message': f'Failed to update employee: {error_msg}'
                }

    def delete_employee(self, employee_id: int) -> Dict[str, Any]:
        """
        Delete an employee by ID.

        Args:
            employee_id: Employee ID to delete

        Returns:
            Dictionary with success status and message
        """
        # Check if employee exists
        existing = employee_repository.get_employee_by_id(employee_id)
        if not existing:
            return {
                'success': False,
                'message': f'Employee with ID {employee_id} not found'
            }

        try:
            success = employee_repository.delete_employee(employee_id)

            if success:
                return {
                    'success': True,
                    'message': f'Employee {employee_id} deleted successfully'
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to delete employee'
                }

        except Exception as e:
            logger.error(f"Service error deleting employee: {e}")
            return {
                'success': False,
                'message': f'Failed to delete employee: {str(e)}'
            }


# Global service instance
employee_service = EmployeeService()
