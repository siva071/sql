"""Reporting service layer for analytics and statistics."""
import logging
import os
from typing import List, Dict, Any, Optional
from repositories.reporting_repository import reporting_repository
from utils.export_utils import (
    export_to_csv,
    export_to_excel,
    format_employee_data_for_export,
    format_department_summary_for_export
)

logger = logging.getLogger(__name__)


class ReportingService:
    """Service layer for reporting and analytics business logic."""

    def get_dashboard_stats(self) -> Dict[str, Any]:
        """
        Get dashboard statistics.

        Returns:
            Dictionary with dashboard statistics
        """
        try:
            stats = reporting_repository.get_dashboard_stats()
            # Convert any None values to 0 for display
            for key, value in stats.items():
                if value is None:
                    stats[key] = 0
            return stats
        except Exception as e:
            logger.error(f"Service error fetching dashboard stats: {e}")
            raise

    def get_department_counts(self) -> List[Dict[str, Any]]:
        """
        Get department employee counts.

        Returns:
            List of department count dictionaries
        """
        try:
            return reporting_repository.get_department_counts()
        except Exception as e:
            logger.error(f"Service error fetching department counts: {e}")
            raise

    def get_department_salary_stats(self) -> List[Dict[str, Any]]:
        """
        Get department salary statistics.

        Returns:
            List of department salary statistics dictionaries
        """
        try:
            return reporting_repository.get_department_salary_stats()
        except Exception as e:
            logger.error(f"Service error fetching department salary stats: {e}")
            raise

    def get_employees_above_dept_avg(self) -> List[Dict[str, Any]]:
        """
        Get employees earning above department average.

        Returns:
            List of employee dictionaries with salary comparison
        """
        try:
            return reporting_repository.get_employees_above_dept_avg()
        except Exception as e:
            logger.error(f"Service error fetching employees above dept avg: {e}")
            raise

    def get_hiring_trends(self) -> List[Dict[str, Any]]:
        """
        Get hiring trends by year.

        Returns:
            List of hiring trend dictionaries
        """
        try:
            return reporting_repository.get_hiring_trends()
        except Exception as e:
            logger.error(f"Service error fetching hiring trends: {e}")
            raise

    def get_all_departments(self) -> List[Dict[str, Any]]:
        """
        Get all departments for dropdown/filter.

        Returns:
            List of department dictionaries
        """
        try:
            return reporting_repository.get_all_departments()
        except Exception as e:
            logger.error(f"Service error fetching departments: {e}")
            raise

    def export_employees_csv(self, employees: List[Dict[str, Any]]) -> str:
        """
        Export employees to CSV.

        Args:
            employees: List of employee dictionaries

        Returns:
            Path to the exported CSV file
        """
        try:
            formatted_data = format_employee_data_for_export(employees)
            return export_to_csv(formatted_data, "employees")
        except Exception as e:
            logger.error(f"Service error exporting employees to CSV: {e}")
            raise

    def export_employees_excel(self, employees: List[Dict[str, Any]]) -> str:
        """
        Export employees to Excel.

        Args:
            employees: List of employee dictionaries

        Returns:
            Path to the exported Excel file
        """
        try:
            formatted_data = format_employee_data_for_export(employees)
            return export_to_excel(formatted_data, "employees")
        except Exception as e:
            logger.error(f"Service error exporting employees to Excel: {e}")
            raise

    def export_department_summary_csv(self, departments: List[Dict[str, Any]]) -> str:
        """
        Export department summary to CSV.

        Args:
            departments: List of department statistics dictionaries

        Returns:
            Path to the exported CSV file
        """
        try:
            formatted_data = format_department_summary_for_export(departments)
            return export_to_csv(formatted_data, "department_summary")
        except Exception as e:
            logger.error(f"Service error exporting department summary to CSV: {e}")
            raise

    def export_department_summary_excel(self, departments: List[Dict[str, Any]]) -> str:
        """
        Export department summary to Excel.

        Args:
            departments: List of department statistics dictionaries

        Returns:
            Path to the exported Excel file
        """
        try:
            formatted_data = format_department_summary_for_export(departments)
            return export_to_excel(formatted_data, "department_summary")
        except Exception as e:
            logger.error(f"Service error exporting department summary to Excel: {e}")
            raise

    def call_plsql_dept_avg(self, department_id: int) -> Optional[float]:
        """
        Call PL/SQL function for department average salary.

        Args:
            department_id: Department ID

        Returns:
            Average salary or None if function not available
        """
        try:
            return reporting_repository.call_plsql_function_dept_avg(department_id)
        except Exception as e:
            logger.warning(f"PL/SQL function call failed: {e}")
            return None


# Global service instance
reporting_service = ReportingService()
