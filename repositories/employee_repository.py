"""Employee repository for database operations (PostgreSQL)."""
import logging
from typing import List, Dict, Any, Optional
import psycopg2
from database.connection import db_connection

logger = logging.getLogger(__name__)


class EmployeeRepository:
    """Repository for employee data access."""

    def get_all_employees(self) -> List[Dict[str, Any]]:
        """
        Retrieve all employees with department information.

        Returns:
            List of employee dictionaries
        """
        query = """
            SELECT e.employee_id, e.first_name, e.last_name, e.email,
                   d.department_name, e.salary, e.hire_date, e.department_id
            FROM employees e
            JOIN departments d ON e.department_id = d.department_id
            ORDER BY e.employee_id
        """

        try:
            with db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)

                columns = [col[0].lower() for col in cursor.description]
                rows = cursor.fetchall()

                employees = []
                for row in rows:
                    emp_dict = dict(zip(columns, row))
                    employees.append(emp_dict)

                return employees
        except Exception as e:
            logger.error(f"Error fetching employees: {e}")
            raise

    def get_employee_by_id(self, employee_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single employee by ID.

        Args:
            employee_id: Employee ID

        Returns:
            Employee dictionary or None if not found
        """
        query = """
            SELECT e.employee_id, e.first_name, e.last_name, e.email,
                   d.department_name, e.salary, e.hire_date, e.department_id
            FROM employees e
            JOIN departments d ON e.department_id = d.department_id
            WHERE e.employee_id = %(employee_id)s
        """

        try:
            with db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, {'employee_id': employee_id})

                row = cursor.fetchone()
                if row:
                    columns = [col[0].lower() for col in cursor.description]
                    return dict(zip(columns, row))
                return None
        except Exception as e:
            logger.error(f"Error fetching employee {employee_id}: {e}")
            raise

    def search_employees(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search employees by name or ID.

        Args:
            search_term: Search term (name or ID)

        Returns:
            List of matching employee dictionaries
        """
        query = """
            SELECT e.employee_id, e.first_name, e.last_name, e.email,
                   d.department_name, e.salary, e.hire_date, e.department_id
            FROM employees e
            JOIN departments d ON e.department_id = d.department_id
            WHERE UPPER(e.first_name) LIKE UPPER(%(search_term)s)
               OR UPPER(e.last_name) LIKE UPPER(%(search_term)s)
               OR e.employee_id::TEXT LIKE %(search_term)s
            ORDER BY e.employee_id
        """

        try:
            with db_connection.get_connection() as conn:
                cursor = conn.cursor()
                search_pattern = f"%{search_term}%"
                cursor.execute(query, {'search_term': search_pattern})

                columns = [col[0].lower() for col in cursor.description]
                rows = cursor.fetchall()

                employees = []
                for row in rows:
                    emp_dict = dict(zip(columns, row))
                    employees.append(emp_dict)

                return employees
        except Exception as e:
            logger.error(f"Error searching employees: {e}")
            raise

    def filter_employees(
        self,
        department_id: Optional[int] = None,
        min_salary: Optional[float] = None,
        max_salary: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Filter employees by department and salary range.

        Args:
            department_id: Optional department ID filter
            min_salary: Optional minimum salary filter
            max_salary: Optional maximum salary filter

        Returns:
            List of filtered employee dictionaries
        """
        query = """
            SELECT e.employee_id, e.first_name, e.last_name, e.email,
                   d.department_name, e.salary, e.hire_date, e.department_id
            FROM employees e
            JOIN departments d ON e.department_id = d.department_id
            WHERE 1=1
        """
        params = {}

        if department_id:
            query += " AND e.department_id = %(department_id)s"
            params['department_id'] = department_id

        if min_salary:
            query += " AND e.salary >= %(min_salary)s"
            params['min_salary'] = min_salary

        if max_salary:
            query += " AND e.salary <= %(max_salary)s"
            params['max_salary'] = max_salary

        query += " ORDER BY e.employee_id"

        try:
            with db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)

                columns = [col[0].lower() for col in cursor.description]
                rows = cursor.fetchall()

                employees = []
                for row in rows:
                    emp_dict = dict(zip(columns, row))
                    employees.append(emp_dict)

                return employees
        except Exception as e:
            logger.error(f"Error filtering employees: {e}")
            raise

    def create_employee(
        self,
        first_name: str,
        last_name: str,
        email: str,
        department_id: int,
        salary: float,
        hire_date: str
    ) -> int:
        """
        Create a new employee.

        Args:
            first_name: Employee first name
            last_name: Employee last name
            email: Employee email
            department_id: Department ID
            salary: Employee salary
            hire_date: Hire date (string in YYYY-MM-DD format)

        Returns:
            New employee ID

        Raises:
            Exception: If creation fails (e.g., duplicate email)
        """
        query = """
            INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(department_id)s, %(salary)s, %(hire_date)s::DATE)
            RETURNING employee_id
        """

        try:
            with db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    query,
                    {
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'department_id': department_id,
                        'salary': salary,
                        'hire_date': hire_date
                    }
                )

                conn.commit()
                new_id = cursor.fetchone()[0]
                logger.info(f"Created employee with ID: {new_id}")
                return new_id

        except psycopg2.IntegrityError as e:
            conn.rollback()
            error_msg = str(e)
            if 'unique constraint' in error_msg.lower() or 'duplicate key' in error_msg.lower():
                raise Exception("Email already exists") from e
            else:
                raise Exception(f"Database constraint error: {error_msg}") from e
        except Exception as e:
            conn.rollback()
            logger.error(f"Error creating employee: {e}")
            raise

    def update_employee(
        self,
        employee_id: int,
        first_name: str,
        last_name: str,
        email: str,
        department_id: int,
        salary: float
    ) -> bool:
        """
        Update an existing employee.

        Args:
            employee_id: Employee ID to update
            first_name: New first name
            last_name: New last name
            email: New email
            department_id: New department ID
            salary: New salary

        Returns:
            True if update successful, False otherwise
        """
        query = """
            UPDATE employees
            SET first_name = %(first_name)s,
                last_name = %(last_name)s,
                email = %(email)s,
                department_id = %(department_id)s,
                salary = %(salary)s
            WHERE employee_id = %(employee_id)s
        """

        try:
            with db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    query,
                    {
                        'employee_id': employee_id,
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'department_id': department_id,
                        'salary': salary
                    }
                )

                conn.commit()
                rows_affected = cursor.rowcount
                logger.info(f"Updated employee {employee_id}, rows affected: {rows_affected}")
                return rows_affected > 0

        except psycopg2.IntegrityError as e:
            conn.rollback()
            error_msg = str(e)
            if 'unique constraint' in error_msg.lower() or 'duplicate key' in error_msg.lower():
                raise Exception("Email already exists") from e
            else:
                raise Exception(f"Database constraint error: {error_msg}") from e
        except Exception as e:
            conn.rollback()
            logger.error(f"Error updating employee {employee_id}: {e}")
            raise

    def delete_employee(self, employee_id: int) -> bool:
        """
        Delete an employee by ID.

        Args:
            employee_id: Employee ID to delete

        Returns:
            True if deletion successful, False otherwise
        """
        query = "DELETE FROM employees WHERE employee_id = %(employee_id)s"

        try:
            with db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, {'employee_id': employee_id})

                conn.commit()
                rows_affected = cursor.rowcount
                logger.info(f"Deleted employee {employee_id}, rows affected: {rows_affected}")
                return rows_affected > 0

        except Exception as e:
            conn.rollback()
            logger.error(f"Error deleting employee {employee_id}: {e}")
            raise


# Global repository instance
employee_repository = EmployeeRepository()
