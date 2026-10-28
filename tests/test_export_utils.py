"""Tests for export utilities module."""
import pytest
import os
from utils.export_utils import (
    export_to_csv,
    export_to_excel,
    format_employee_data_for_export,
    format_department_summary_for_export
)


class TestEmployeeDataFormatting:
    """Test employee data formatting for export."""

    def test_format_employee_data(self):
        """Test formatting employee data."""
        employees = [
            {
                'employee_id': 1,
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'department_name': 'Engineering',
                'salary': 75000.00,
                'hire_date': '2020-01-15'
            }
        ]

        formatted = format_employee_data_for_export(employees)

        assert len(formatted) == 1
        assert formatted[0]['Employee ID'] == 1
        assert formatted[0]['First Name'] == 'John'
        assert formatted[0]['Last Name'] == 'Doe'
        assert formatted[0]['Email'] == 'john@example.com'
        assert formatted[0]['Department'] == 'Engineering'
        assert formatted[0]['Salary'] == 75000.00
        assert formatted[0]['Hire Date'] == '2020-01-15'

    def test_format_empty_employee_data(self):
        """Test formatting empty employee data."""
        formatted = format_employee_data_for_export([])
        assert formatted == []


class TestDepartmentSummaryFormatting:
    """Test department summary formatting for export."""

    def test_format_department_summary(self):
        """Test formatting department summary."""
        departments = [
            {
                'department_name': 'Engineering',
                'location': 'Building A',
                'employee_count': 10,
                'avg_salary': 75000.00,
                'min_salary': 50000.00,
                'max_salary': 100000.00,
                'total_payroll': 750000.00
            }
        ]

        formatted = format_department_summary_for_export(departments)

        assert len(formatted) == 1
        assert formatted[0]['Department'] == 'Engineering'
        assert formatted[0]['Location'] == 'Building A'
        assert formatted[0]['Employee Count'] == 10
        assert formatted[0]['Average Salary'] == 75000.00
        assert formatted[0]['Minimum Salary'] == 50000.00
        assert formatted[0]['Maximum Salary'] == 100000.00
        assert formatted[0]['Total Payroll'] == 750000.00

    def test_format_empty_department_summary(self):
        """Test formatting empty department summary."""
        formatted = format_department_summary_for_export([])
        assert formatted == []


class TestCSVExport:
    """Test CSV export functionality."""

    def test_export_to_csv(self, tmp_path):
        """Test exporting data to CSV."""
        data = [
            {'name': 'John', 'salary': 50000},
            {'name': 'Jane', 'salary': 60000}
        ]

        # Change to temp directory for test
        original_dir = os.getcwd()
        os.chdir(tmp_path)
        os.makedirs('reports', exist_ok=True)

        try:
            filepath = export_to_csv(data, "test_report")

            assert filepath.endswith('.csv')
            assert os.path.exists(filepath)
            assert 'test_report' in filepath

        finally:
            os.chdir(original_dir)

    def test_export_empty_data_to_csv(self):
        """Test exporting empty data to CSV (should raise error)."""
        with pytest.raises(ValueError, match="No data to export"):
            export_to_csv([], "test_report")


class TestExcelExport:
    """Test Excel export functionality."""

    def test_export_to_excel(self, tmp_path):
        """Test exporting data to Excel."""
        data = [
            {'name': 'John', 'salary': 50000},
            {'name': 'Jane', 'salary': 60000}
        ]

        # Change to temp directory for test
        original_dir = os.getcwd()
        os.chdir(tmp_path)
        os.makedirs('reports', exist_ok=True)

        try:
            filepath = export_to_excel(data, "test_report")

            assert filepath.endswith('.xlsx')
            assert os.path.exists(filepath)
            assert 'test_report' in filepath

        finally:
            os.chdir(original_dir)

    def test_export_empty_data_to_excel(self):
        """Test exporting empty data to Excel (should raise error)."""
        with pytest.raises(ValueError, match="No data to export"):
            export_to_excel([], "test_report")
