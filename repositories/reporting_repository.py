"""Reporting repository for analytics and statistics (PostgreSQL)."""
import logging
from typing import List, Dict, Any, Optional
import psycopg2
from database.connection import db_connection

logger = logging.getLogger(__name__)


class ReportingRepository:
    """Repository for reporting and analytics data access."""

    def get_dashboard_stats(self) -> Dict[str, Any]:
        """
        Get overall dashboard statistics.

        Returns:
            Dictionary with total employees, departments, average salary, etc.
        """
        query = """
            SELECT
                (SELECT COUNT(*) FROM employees) AS total_employees,
                (SELECT COUNT(*) FROM departments) AS total_departments,
                (SELECT ROUND(AVG(salary), 2) FROM employees) AS avg_salary,
                (SELECT MAX(salary) FROM employees) AS max_salary,
                (SELECT MIN(salary) FROM employees) AS min_salary,
                (SELECT ROUND(SUM(salary), 2) FROM employees) AS total_payroll
        """

        try:
            with db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)

                row = cursor.fetchone()
                if row:
                    columns = [col[0].lower() for col in cursor.description]
                    stats = dict(zip(columns, row))
                    # Convert None to 0 for display
                    for key, value in stats.items():
                        if value is None:
                            stats[key] = 0
                    return stats
                return {
                    'total_employees': 0,
                    'total_departments': 0,
                    'avg_salary': 0,
                    'max_salary': 0,
                    'min_salary': 0,
                    'total_payroll': 0
                }
        except Exception as e:
            logger.error(f"Error fetching dashboard stats: {e}")
            raise

    def get_department_counts(self) -> List[Dict[str, Any]]:
        """
        Get employee count per department.

        Returns:
            List of department count dictionaries
        """
        query = """
            SELECT
                d.department_name,
                COUNT(e.employee_id) AS employee_count
            FROM departments d
            LEFT JOIN employees e ON d.department_id = e.department_id
            GROUP BY d.department_name
            ORDER BY employee_count DESC
        """

        try:
            with db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)

                columns = [col[0].lower() for col in cursor.description]
                rows = cursor.fetchall()

                dept_counts = []
                for row in rows:
                    dept_dict = dict(zip(columns, row))
                    dept_counts.append(dept_dict)

                return dept_counts
        except Exception as e:
            logger.error(f"Error fetching department counts: {e}")
            raise

    def get_department_salary_stats(self) -> List[Dict[str, Any]]:
        """
        Get salary statistics per department.

        Returns:
            List of department salary statistics dictionaries
        """
        query = """
            SELECT
                d.department_name,
                COUNT(e.employee_id) AS employee_count,
                ROUND(AVG(e.salary), 2) AS avg_salary,
                MIN(e.salary) AS min_salary,
                MAX(e.salary) AS max_salary,
                ROUND(SUM(e.salary), 2) AS total_payroll
            FROM departments d
            LEFT JOIN employees e ON d.department_id = e.department_id
            GROUP BY d.department_name
            ORDER BY avg_salary DESC
        """

        try:
            with db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)

                columns = [col[0].lower() for col in cursor.description]
                rows = cursor.fetchall()

                salary_stats = []
                for row in rows:
                    stats_dict = dict(zip(columns, row))
                    salary_stats.append(stats_dict)

                return salary_stats
        except Exception as e:
            logger.error(f"Error fetching department salary stats: {e}")
            raise

    def get_employees_above_dept_avg(self) -> List[Dict[str, Any]]:
        """
        Get employees earning above their department average.

        Returns:
            List of employee dictionaries with salary comparison
        """
        query = """
            WITH dept_avg AS (
                SELECT
                    department_id,
                    AVG(salary) AS avg_salary
                FROM employees
                GROUP BY department_id
            )
            SELECT
                e.employee_id,
                e.first_name,
                e.last_name,
                d.department_name,
                e.salary,
                da.avg_salary AS department_avg,
                ROUND(e.salary - da.avg_salary, 2) AS salary_difference
            FROM employees e
            JOIN departments d ON e.department_id = d.department_id
            JOIN dept_avg da ON e.department_id = da.department_id
            WHERE e.salary > da.avg_salary
            ORDER BY salary_difference DESC
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
            logger.error(f"Error fetching employees above dept avg: {e}")
            raise

    def get_hiring_trends(self) -> List[Dict[str, Any]]:
        """
        Get hiring trends by year.

        Returns:
            List of hiring trend dictionaries
        """
        query = """
            SELECT
                EXTRACT(YEAR FROM hire_date)::INTEGER AS hire_year,
                COUNT(*) AS hires_count
            FROM employees
            GROUP BY EXTRACT(YEAR FROM hire_date)
            ORDER BY hire_year
        """

        try:
            with db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)

                columns = [col[0].lower() for col in cursor.description]
                rows = cursor.fetchall()

                trends = []
                for row in rows:
                    trend_dict = dict(zip(columns, row))
                    trends.append(trend_dict)

                return trends
        except Exception as e:
            logger.error(f"Error fetching hiring trends: {e}")
            raise

    def get_all_departments(self) -> List[Dict[str, Any]]:
        """
        Get all departments.

        Returns:
            List of department dictionaries
        """
        query = """
            SELECT department_id, department_name, location
            FROM departments
            ORDER BY department_name
        """

        try:
            with db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)

                columns = [col[0].lower() for col in cursor.description]
                rows = cursor.fetchall()

                departments = []
                for row in rows:
                    dept_dict = dict(zip(columns, row))
                    departments.append(dept_dict)

                return departments
        except Exception as e:
            logger.error(f"Error fetching departments: {e}")
            raise

    def call_plsql_function_dept_avg(self, department_id: int) -> Optional[float]:
        """
        Call PostgreSQL function to get department average salary.

        Args:
            department_id: Department ID

        Returns:
            Average salary or None if function fails
        """
        try:
            with db_connection.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT fn_dept_avg_salary(%s)", (department_id,))
                result = cursor.fetchone()
                return float(result[0]) if result and result[0] else None
        except Exception as e:
            logger.warning(f"PostgreSQL function call failed (may not be installed): {e}")
            return None


# Global repository instance
reporting_repository = ReportingRepository()
