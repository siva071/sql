# Python + PostgreSQL Employee Reporting System (Neon)

A complete, production-ready employee reporting application built with Python, PostgreSQL (Neon), and Streamlit. This project demonstrates database connectivity, SQL fundamentals, PL/pgSQL, data analysis, and web application development with free cloud deployment capability.

## Project Overview

This application provides a comprehensive employee management and reporting system with the following features:

- **Dashboard**: Real-time statistics on employees, departments, salaries, and hiring trends
- **Employee Management**: View, add, update, and delete employee records with validation
- **Advanced Filtering**: Search by name/ID, filter by department and salary range
- **SQL Reports**: Department-wise analysis, high earners, hiring trends
- **Export Functionality**: Download reports as CSV or Excel files
- **PL/pgSQL Integration**: Stored functions for advanced reporting
- **Cloud-Ready**: Deployable to Neon PostgreSQL for free hosting

## Technology Stack

- **Language**: Python 3.10+
- **Database**: PostgreSQL (Neon Serverless PostgreSQL)
- **Web Framework**: Streamlit 1.39.0
- **Database Driver**: psycopg2-binary 2.9.9
- **Data Processing**: Pandas 2.2.3
- **Testing**: pytest 8.3.3, pytest-mock 3.14.0
- **Excel Export**: openpyxl 3.1.5
- **Configuration**: python-dotenv 1.0.1

## Architecture

The project follows a layered architecture with separation of concerns:

```
python-postgres-reporting-system/
├── app.py                          # Streamlit dashboard (UI layer)
├── config/
│   ├── __init__.py
│   └── settings.py                 # Environment-based configuration
├── database/
│   ├── __init__.py
│   ├── connection.py              # PostgreSQL connection management
│   └── schema_notes.md            # Database schema documentation
├── repositories/                   # Data access layer
│   ├── __init__.py
│   ├── employee_repository.py     # Employee CRUD operations
│   └── reporting_repository.py    # Analytics and statistics queries
├── services/                       # Business logic layer
│   ├── __init__.py
│   ├── employee_service.py        # Employee business logic
│   └── reporting_service.py       # Reporting business logic
├── utils/                          # Utility functions
│   ├── __init__.py
│   ├── validators.py              # Input validation
│   └── export_utils.py           # CSV/Excel export
├── sql/                            # Database scripts
│   ├── 01_create_schema_postgres.sql    # PostgreSQL table creation
│   ├── 02_seed_sample_data_postgres.sql  # Sample data
│   ├── 03_plsql_objects_postgres.sql    # PostgreSQL functions
│   └── oracle_backup/                      # Original Oracle scripts (backup)
│       ├── 01_create_schema.sql
│       ├── 02_create_tables.sql
│       ├── 03_seed_sample_data.sql
│       ├── 04_reporting_queries.sql
│       └── 05_plsql_objects.sql
├── tests/                          # Unit tests
│   ├── __init__.py
│   ├── test_validators.py
│   ├── test_export_utils.py
│   └── test_employee_service.py
├── reports/                        # Generated reports (created at runtime)
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## Prerequisites

Before setting up this project, ensure you have:

1. **Python 3.10 or higher** installed on Windows
2. **Git** for version control
3. **Neon PostgreSQL account** (free at https://neon.tech)
4. Administrator permissions (not required for Neon)

## Windows Setup Guide

### Step 1: Create Neon PostgreSQL Account

1. Visit: https://neon.tech
2. Sign up for a free account
3. Create a new project
4. Note the connection string from the Neon dashboard
5. Format: `postgresql://username:password@host/database?sslmode=require`

### Step 2: Clone or Download the Project

If you have this project from Git:
```bash
git clone <repository-url>
cd sql
```

Or navigate to the project directory.

### Step 3: Create Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate Virtual Environment

On Windows:
```bash
venv\Scripts\activate
```

You should see `(venv)` in your command prompt.

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required Python packages.

### Step 6: Configure Environment Variables

1. Copy the example environment file:
```bash
copy .env.example .env
```

2. Edit `.env` with your Neon database credentials:
```env
DATABASE_URL=postgresql://your_username:your_password@your_host:5432/your_database?sslmode=require
```

**Important**: Never commit `.env` to Git!

### Step 7: Create Database Schema

Run the PostgreSQL setup script:
```bash
python setup_postgres_database.py
```

This will:
- Create departments and employees tables
- Insert 6 departments and 20 sample employees
- Create PostgreSQL functions equivalent to Oracle PL/SQL

The script is idempotent - safe to rerun.

## Running the Application

### Start the Streamlit Application

With your virtual environment activated:

```bash
streamlit run app.py
```

The application will start and open in your default web browser at:
http://localhost:8501

### Application Navigation

The dashboard has three main sections:

1. **Dashboard**: Overview statistics and visualizations
2. **Employee Management**: CRUD operations for employees
3. **Reports**: Advanced analytics and export options

## Running Tests

### Run All Tests

```bash
python -m pytest tests/ -v
```

### Run Specific Test File

```bash
python -m pytest tests/test_validators.py -v
```

### Test Results

**Current Status**: 41/41 tests passing (100% pass rate)

The tests use mocks for database operations, so they run without requiring a live database connection.

## Database Schema

### Tables

1. **departments**
   - department_id (SERIAL PRIMARY KEY)
   - department_name (VARCHAR(50) UNIQUE, NOT NULL)
   - location (VARCHAR(100))

2. **employees**
   - employee_id (SERIAL PRIMARY KEY)
   - first_name (VARCHAR(50) NOT NULL)
   - last_name (VARCHAR(50) NOT NULL)
   - email (VARCHAR(100) UNIQUE, NOT NULL)
   - department_id (INTEGER NOT NULL)
   - salary (NUMERIC(10,2) NOT NULL, CHECK > 0)
   - hire_date (DATE NOT NULL)
   - FOREIGN KEY to departments

### PostgreSQL Functions (PL/pgSQL)

1. **fn_dept_avg_salary(department_id)** - Returns average salary for a department
2. **fn_employee_count(department_id)** - Returns employee count for a department
3. **sp_insert_employee(...)** - Inserts employee with validation (returns JSON)
4. **sp_update_employee_salary(...)** - Updates salary with validation (returns JSON)
5. **sp_department_report(department_id)** - Returns department statistics (SETOF)

All functions are equivalent to the original Oracle PL/SQL objects.

## SQL Query Examples

The `oracle_backup/04_reporting_queries.sql` file contains Oracle-specific examples. For PostgreSQL, the key differences are:

- **Parameter style**: PostgreSQL uses `%(param)s` instead of `:param`
- **Date literals**: PostgreSQL uses `'YYYY-MM-DD'::DATE` instead of `TO_DATE('YYYY-MM-DD', 'YYYY-MM-DD')`
- **Identity**: PostgreSQL uses `SERIAL` or `GENERATED ALWAYS AS IDENTITY` (similar to Oracle)
- **Functions**: PostgreSQL uses `RETURN` without semicolon in PL/pgSQL

## Deployment to Streamlit Cloud

### Step 1: Prepare for Deployment

1. Ensure your `.env` is not committed to Git
2. Create a GitHub repository and push your code
3. Your repository should have:
   - app.py
   - requirements.txt
   - All Python modules
   - sql/ folder with PostgreSQL scripts
   - .env.example (with DATABASE_URL placeholder)

### Step 2: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in and connect your GitHub repository
3. Streamlit Cloud will automatically:
   - Install dependencies from requirements.txt
   - Run app.py
   - Provide a public URL

### Step 3: Configure Environment Variables

In Streamlit Cloud:
1. Go to your app settings
2. Add environment variable: `DATABASE_URL`
3. Paste your Neon connection string
4. Restart the app

### Step 4: Set Up Neon Database

If you haven't already:
1. Log in to Neon
2. Create a new project (or use existing)
3. Copy the connection string
4. Add it to Streamlit Cloud environment variables

## Troubleshooting

### Database Connection Issues

**Error**: "Cannot connect to PostgreSQL Database"

**Solutions**:
1. Verify Neon account is active
2. Check your DATABASE_URL in .env
3. Ensure SSL is enabled (sslmode=require)
4. Test connection: `python -c "import psycopg2; from config.settings import settings; psycopg2.connect(settings.DATABASE_URL)"`

### SSL Certificate Errors

**Error**: SSL certificate verification failed

**Solutions**:
1. Ensure `sslmode=require` is in your connection string
2. If using a self-signed cert, use `sslmode=no-verify` (not recommended for production)

### Port Already in Use

**Error**: "Port 8501 is already in use"

**Solution**: Use a different port:
```bash
streamlit run app.py --server.port 8502
```

## Security Considerations

1. **Never commit `.env`** - It contains database credentials
2. **Use strong passwords** for database users
3. **Limit database user permissions** - Only grant necessary privileges
4. **Parameterized queries** - All SQL uses parameterized statements to prevent SQL injection
5. **Input validation** - All user inputs are validated before database operations
6. **No logging of sensitive data** - Passwords are never logged or displayed

## Migration from Oracle

This project was migrated from Oracle Database to PostgreSQL/Neon. The original Oracle SQL scripts are preserved in the `oracle_backup/` folder.

### Key Changes:

1. **Database Driver**: Changed from `oracledb` to `psycopg2-binary`
2. **Data Types**: Oracle `NUMBER` → PostgreSQL `NUMERIC`, `VARCHAR2` → `VARCHAR`
3. **Identity**: Oracle `GENERATED ALWAYS AS IDENTITY` → PostgreSQL `SERIAL`
4. **Parameters**: Oracle `:param` → PostgreSQL `%(param)s`
5. **PL/SQL**: Oracle procedures → PostgreSQL functions (simplified)
6. **Connection**: Oracle DSN → PostgreSQL connection string

All features are preserved and functional.

## Known Limitations

1. **PL/SQL Functions**: PostgreSQL functions work differently than Oracle procedures. The application handles this gracefully.
2. **Date Handling**: PostgreSQL date functions are slightly different but compatible
3. **No Authentication**: No user authentication or authorization implemented
4. **Single User**: No concurrent user handling

## File Changes Summary

### Modified Files:
- `requirements.txt` - Switched to psycopg2-binary
- `config/settings.py` - Added DATABASE_URL support
- `database/connection.py` - Rewritten for psycopg2
- `repositories/employee_repository.py` - Updated for PostgreSQL parameter syntax
- `repositories/reporting_repository.py` - Updated for PostgreSQL
- `.env.example` - Updated for PostgreSQL configuration
- `README.md` - Updated for PostgreSQL/Neon

### New Files:
- `sql/01_create_schema_postgres.sql` - PostgreSQL DDL
- `sql/02_seed_sample_data_postgres.sql` - PostgreSQL seed data
- `sql/03_plsql_objects_postgres.sql` - PostgreSQL functions
- `setup_postgres_database.py` - PostgreSQL setup script
- `oracle_backup/` - Backup of original Oracle scripts

### Unchanged Files:
- `app.py` - No changes needed
- `services/` - No changes needed
- `utils/` - No changes needed
- `tests/` - No changes needed (tests use mocks)

## Testing Commands

To run the migrated application:

```bash
# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure .env with Neon DATABASE_URL
# (copy .env.example to .env and edit)

# Set up database
python setup_postgres_database.py

# Run tests
python -m pytest tests/ -v

# Start application
streamlit run app.py
```

## Interview Preparation

When explaining this project in an interview:

1. **Architecture**: Explain the layered architecture (UI, Service, Repository, Database)
2. **Technology Choices**: Why PostgreSQL/Neon (free cloud hosting, easier deployment)
3. **Challenges**: Migrating from Oracle to PostgreSQL, parameter syntax differences
4. **Learning**: PostgreSQL differences from Oracle, cloud database management
5. **Improvements**: What you would add (authentication, pagination, more reports)

Example talking points:
- "I built a complete employee reporting system using Python and PostgreSQL/Neon"
- "The application uses a layered architecture with separation of concerns"
- "I implemented comprehensive input validation and parameterized queries for security"
- "The SQL module demonstrates GROUP BY, JOINs, subqueries, and CTEs"
- "I also implemented PostgreSQL stored functions for advanced reporting"
- "The application is cloud-ready and can be deployed to Streamlit Cloud with Neon PostgreSQL"

## SQL and PL/pgSQL Concepts for Resume

Before claiming SQL and PostgreSQL skills on your resume, ensure you understand:

### SQL Fundamentals
- SELECT and WHERE
- ORDER BY
- GROUP BY and HAVING
- Aggregate functions: COUNT, SUM, AVG, MIN, MAX
- INNER JOIN and LEFT JOIN
- Subqueries
- Common Table Expressions (CTE)
- Date functions: EXTRACT, date casting

### Database Design
- Primary keys and foreign keys
- UNIQUE constraints
- CHECK constraints
- SERIAL identity columns
- Indexes for performance

### PL/pgSQL (PostgreSQL)
- Stored functions (not procedures like Oracle)
- RETURN statement
- Exception handling
- JSON return types (for complex results)
- SETOF return types (for table results)

### Python Database Integration
- Connection management using psycopg2
- Parameterized queries (using %(param)s)
- Transaction handling (commit and rollback)
- Error management

## Support and Resources

- **Neon Documentation**: https://neon.tech/docs
- **psycopg2 Documentation**: https://www.psycopg.org/docs/
- **Streamlit Documentation**: https://docs.streamlit.io/
- **Python Documentation**: https://docs.python.org/3/

## License

This project is for educational purposes. Feel free to use it as a template for your own projects.

---

**Built with Python, PostgreSQL (Neon), and Streamlit**
