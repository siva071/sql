# Database Schema Notes

## User Creation

Before running the SQL scripts, create a dedicated application user:

```sql
-- Connect as SYS or SYSTEM
CREATE USER hr_app IDENTIFIED BY "YourSecurePassword123";
GRANT CONNECT, RESOURCE TO hr_app;
GRANT CREATE SESSION TO hr_app;
GRANT CREATE TABLE TO hr_app;
GRANT CREATE SEQUENCE TO hr_app;
GRANT CREATE PROCEDURE TO hr_app;
GRANT CREATE VIEW TO hr_app;
```

## Schema Overview

### Tables

1. **departments**
   - department_id (PRIMARY KEY)
   - department_name (UNIQUE, NOT NULL)
   - location

2. **employees**
   - employee_id (PRIMARY KEY)
   - first_name (NOT NULL)
   - last_name (NOT NULL)
   - email (UNIQUE, NOT NULL)
   - department_id (FOREIGN KEY)
   - salary (CHECK constraint for positive values)
   - hire_date (NOT NULL)

### Relationships

- One department can have many employees
- Each employee belongs to exactly one department

## SQL Script Execution Order

1. 01_create_schema.sql - Create tables with constraints
2. 02_create_tables.sql - Additional indexes if needed
3. 03_seed_sample_data.sql - Insert sample data
4. 04_reporting_queries.sql - These are queries, not DDL
5. 05_plsql_objects.sql - Create stored procedures and functions

## Connection Notes

- python-oracledb thin mode is used (no Oracle Instant Client required)
- Connection string format: host:port/service_name
- Default Oracle Database Free service name: FREEPDB1
- Alternative service name: XEPDB1 (some installations)
