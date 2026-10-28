"""Streamlit dashboard for Employee Reporting System."""
import streamlit as st
import pandas as pd
from datetime import datetime
import os

from services.employee_service import employee_service
from services.reporting_service import reporting_service
from database.connection import db_connection

# Page configuration
st.set_page_config(
    page_title="Employee Reporting System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def check_database_connection():
    """Check if database connection is available."""
    try:
        with db_connection.get_connection() as conn:
            if conn:
                return True
    except Exception as e:
        st.error(f"Database connection failed: {str(e)}")
        st.error("Please check your .env file and ensure Oracle Database is running.")
        st.info("See README.md for database setup instructions.")
        return False
    return False


def display_dashboard():
    """Display main dashboard with statistics."""
    st.markdown('<h1 class="main-header">📊 Employee Dashboard</h1>', unsafe_allow_html=True)

    try:
        # Get dashboard statistics
        stats = reporting_service.get_dashboard_stats()

        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Employees", stats.get('total_employees', 0))
        with col2:
            st.metric("Total Departments", stats.get('total_departments', 0))
        with col3:
            st.metric("Average Salary", f"${stats.get('avg_salary', 0):,.2f}")
        with col4:
            st.metric("Highest Salary", f"${stats.get('max_salary', 0):,.2f}")

        st.markdown("---")

        # Department counts
        dept_counts = reporting_service.get_department_counts()
        if dept_counts:
            st.subheader("Employee Count by Department")
            dept_df = pd.DataFrame(dept_counts)
            st.bar_chart(dept_df.set_index('department_name')['employee_count'])

        # Department salary statistics
        st.markdown("---")
        salary_stats = reporting_service.get_department_salary_stats()
        if salary_stats:
            st.subheader("Department Salary Statistics")
            salary_df = pd.DataFrame(salary_stats)
            st.dataframe(salary_df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")


def display_employee_management():
    """Display employee management section."""
    st.markdown('<h1 class="main-header">👥 Employee Management</h1>', unsafe_allow_html=True)

    # Tabs for different operations
    tab1, tab2, tab3 = st.tabs(["View Employees", "Add Employee", "Update/Delete"])

    with tab1:
        display_employee_list()

    with tab2:
        display_add_employee_form()

    with tab3:
        display_update_delete_employee()


def display_employee_list():
    """Display list of employees with filters."""
    st.subheader("Employee Directory")

    # Get departments for filter
    departments = reporting_service.get_all_departments()
    dept_options = {0: "All Departments"}
    for dept in departments:
        dept_options[dept['department_id']] = dept['department_name']

    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        search_term = st.text_input("Search by name or ID", placeholder="Enter name or ID...")
    with col2:
        selected_dept = st.selectbox("Filter by Department", options=list(dept_options.keys()),
                                    format_func=lambda x: dept_options[x])
    with col3:
        min_salary = st.number_input("Min Salary", min_value=0, value=0, step=1000)
    with col4:
        max_salary = st.number_input("Max Salary", min_value=0, value=1000000, step=1000)

    clear_filters = st.button("Clear Filters")

    if clear_filters:
        search_term = ""
        selected_dept = 0
        min_salary = 0
        max_salary = 1000000
        st.rerun()

    # Fetch employees
    try:
        if search_term:
            employees = employee_service.search_employees(search_term)
        else:
            dept_filter = selected_dept if selected_dept > 0 else None
            salary_min = min_salary if min_salary > 0 else None
            salary_max = max_salary if max_salary < 1000000 else None
            employees = employee_service.filter_employees(dept_filter, salary_min, salary_max)

        if employees:
            # Display as DataFrame
            df = pd.DataFrame(employees)
            df_display = df[['employee_id', 'first_name', 'last_name', 'email',
                            'department_name', 'salary', 'hire_date']]
            df_display.columns = ['ID', 'First Name', 'Last Name', 'Email',
                                'Department', 'Salary', 'Hire Date']
            st.dataframe(df_display, use_container_width=True, hide_index=True)

            # Export buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Export to CSV", key="export_csv_list"):
                    try:
                        filepath = reporting_service.export_employees_csv(employees)
                        st.success(f"Exported to: {filepath}")
                    except Exception as e:
                        st.error(f"Export failed: {str(e)}")
            with col2:
                if st.button("Export to Excel", key="export_excel_list"):
                    try:
                        filepath = reporting_service.export_employees_excel(employees)
                        st.success(f"Exported to: {filepath}")
                    except Exception as e:
                        st.error(f"Export failed: {str(e)}")
        else:
            st.info("No employees found matching the criteria.")

    except Exception as e:
        st.error(f"Error fetching employees: {str(e)}")


def display_add_employee_form():
    """Display form to add new employee."""
    st.subheader("Add New Employee")

    with st.form("add_employee_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name *")
            email = st.text_input("Email *")
        with col2:
            last_name = st.text_input("Last Name *")
            salary = st.number_input("Salary *", min_value=0.01, value=50000.00, step=1000.00)

        departments = reporting_service.get_all_departments()
        dept_options = {dept['department_id']: dept['department_name'] for dept in departments}
        department_id = st.selectbox("Department *", options=list(dept_options.keys()),
                                     format_func=lambda x: dept_options[x])

        hire_date = st.date_input("Hire Date *", value=datetime.now())

        submitted = st.form_submit_button("Add Employee")

        if submitted:
            hire_date_str = hire_date.strftime('%Y-%m-%d')
            result = employee_service.create_employee(
                first_name=first_name,
                last_name=last_name,
                email=email,
                department_id=department_id,
                salary=salary,
                hire_date=hire_date_str
            )

            if result['success']:
                st.success(result['message'])
                st.rerun()
            else:
                st.error(result['message'])
                if 'errors' in result:
                    for field, error in result['errors'].items():
                        st.error(f"{field}: {error}")


def display_update_delete_employee():
    """Display form to update or delete employee."""
    st.subheader("Update or Delete Employee")

    # Select employee
    employees = employee_service.get_all_employees()
    if not employees:
        st.info("No employees available.")
        return

    emp_options = {emp['employee_id']: f"{emp['first_name']} {emp['last_name']} (ID: {emp['employee_id']})"
                  for emp in employees}
    selected_emp_id = st.selectbox("Select Employee", options=list(emp_options.keys()),
                                  format_func=lambda x: emp_options[x])

    selected_emp = employee_service.get_employee_by_id(selected_emp_id)

    if selected_emp:
        # Display current info
        st.info(f"Current Info: {selected_emp['first_name']} {selected_emp['last_name']} - "
               f"{selected_emp['email']} - {selected_emp['department_name']} - ${selected_emp['salary']:,.2f}")

        col1, col2 = st.columns(2)

        with col1:
            with st.form("update_employee_form"):
                st.subheader("Update Employee")
                first_name = st.text_input("First Name", value=selected_emp['first_name'])
                last_name = st.text_input("Last Name", value=selected_emp['last_name'])
                email = st.text_input("Email", value=selected_emp['email'])
                departments = reporting_service.get_all_departments()
                dept_options = {dept['department_id']: dept['department_name'] for dept in departments}
                department_id = st.selectbox("Department", options=list(dept_options.keys()),
                                           format_func=lambda x: dept_options[x],
                                           index=list(dept_options.keys()).index(selected_emp['department_id']))
                salary = st.number_input("Salary", min_value=0.01, value=float(selected_emp['salary']),
                                       step=1000.00)

                submitted = st.form_submit_button("Update Employee")

                if submitted:
                    result = employee_service.update_employee(
                        employee_id=selected_emp_id,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        department_id=department_id,
                        salary=salary
                    )

                    if result['success']:
                        st.success(result['message'])
                        st.rerun()
                    else:
                        st.error(result['message'])
                        if 'errors' in result:
                            for field, error in result['errors'].items():
                                st.error(f"{field}: {error}")

        with col2:
            st.subheader("Delete Employee")
            st.warning("This action cannot be undone!")
            if st.button(f"Delete Employee {selected_emp_id}", type="primary"):
                result = employee_service.delete_employee(selected_emp_id)
                if result['success']:
                    st.success(result['message'])
                    st.rerun()
                else:
                    st.error(result['message'])


def display_reports():
    """Display reports section."""
    st.markdown('<h1 class="main-header">📈 Reports</h1>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Department Summary", "High Earners", "Hiring Trends"])

    with tab1:
        display_department_summary_report()

    with tab2:
        display_high_earners_report()

    with tab3:
        display_hiring_trends_report()


def display_department_summary_report():
    """Display department summary report."""
    st.subheader("Department Summary Report")

    try:
        dept_stats = reporting_service.get_department_salary_stats()
        if dept_stats:
            df = pd.DataFrame(dept_stats)
            st.dataframe(df, use_container_width=True, hide_index=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Export to CSV", key="export_dept_csv"):
                    try:
                        filepath = reporting_service.export_department_summary_csv(dept_stats)
                        st.success(f"Exported to: {filepath}")
                    except Exception as e:
                        st.error(f"Export failed: {str(e)}")
            with col2:
                if st.button("Export to Excel", key="export_dept_excel"):
                    try:
                        filepath = reporting_service.export_department_summary_excel(dept_stats)
                        st.success(f"Exported to: {filepath}")
                    except Exception as e:
                        st.error(f"Export failed: {str(e)}")
        else:
            st.info("No department data available.")

    except Exception as e:
        st.error(f"Error loading department summary: {str(e)}")


def display_high_earners_report():
    """Display high earners report."""
    st.subheader("Employees Earning Above Department Average")

    try:
        high_earners = reporting_service.get_employees_above_dept_avg()
        if high_earners:
            df = pd.DataFrame(high_earners)
            df_display = df[['first_name', 'last_name', 'department_name', 'salary',
                           'department_avg', 'salary_difference']]
            df_display.columns = ['First Name', 'Last Name', 'Department', 'Salary',
                                'Dept Average', 'Difference']
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        else:
            st.info("No employees earning above department average found.")

    except Exception as e:
        st.error(f"Error loading high earners report: {str(e)}")


def display_hiring_trends_report():
    """Display hiring trends report."""
    st.subheader("Hiring Trends by Year")

    try:
        trends = reporting_service.get_hiring_trends()
        if trends:
            df = pd.DataFrame(trends)
            st.line_chart(df.set_index('hire_year')['hires_count'])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No hiring trend data available.")

    except Exception as e:
        st.error(f"Error loading hiring trends: {str(e)}")


def main():
    """Main application entry point."""
    # Create reports directory if it doesn't exist
    if not os.path.exists('reports'):
        os.makedirs('reports')

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Employee Management", "Reports"])

    # Check database connection
    if not check_database_connection():
        st.stop()

    # Display selected page
    if page == "Dashboard":
        display_dashboard()
    elif page == "Employee Management":
        display_employee_management()
    elif page == "Reports":
        display_reports()


if __name__ == "__main__":
    main()
