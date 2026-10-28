"""Script to execute SQL setup files using python-oracledb."""
import oracledb
from config.settings import settings
import os
import re


def execute_sql_file(filename):
    """Execute a SQL file, handling PL/SQL blocks properly."""
    filepath = os.path.join('sql', filename)
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return False

    print(f"\n{'='*60}")
    print(f"Executing: {filename}")
    print('='*60)

    try:
        conn = oracledb.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            dsn=settings.connection_string
        )
        cursor = conn.cursor()

        with open(filepath, 'r') as f:
            sql_content = f.read()

        # Remove comments
        sql_content = re.sub(r'--.*$', '', sql_content, flags=re.MULTILINE)

        # Split by forward slash (Oracle convention for statement separators)
        # This handles PL/SQL blocks that contain semicolons
        statements = []
        current_statement = []
        in_plsql_block = False

        for line in sql_content.split('\n'):
            line = line.strip()
            if not line:
                continue

            # Detect PL/SQL block start
            if line.upper().startswith(('DECLARE', 'BEGIN', 'CREATE OR REPLACE', 'CREATE PROCEDURE', 'CREATE FUNCTION')):
                in_plsql_block = True

            current_statement.append(line)

            # Statement separator is /
            if line == '/':
                statement = '\n'.join(current_statement[:-1])  # Exclude the /
                if statement.strip():
                    statements.append(statement.strip())
                current_statement = []
                in_plsql_block = False
            # For simple SQL statements (not in PL/SQL block), end with ;
            elif line.endswith(';') and not in_plsql_block:
                statement = '\n'.join(current_statement)
                if statement.strip():
                    statements.append(statement.strip())
                current_statement = []

        # Add any remaining statement
        if current_statement:
            statement = '\n'.join(current_statement)
            if statement.strip():
                statements.append(statement.strip())

        print(f"Found {len(statements)} statements to execute")

        for i, stmt in enumerate(statements, 1):
            if not stmt or stmt.upper().startswith('COMMIT'):
                continue

            try:
                cursor.execute(stmt)
                conn.commit()
                print(f"[OK] Statement {i}/{len(statements)} executed")
            except Exception as e:
                error_msg = str(e)
                if 'ORA-00942' in error_msg and 'DROP' in stmt.upper():
                    # Ignore drop errors for non-existent tables
                    print(f"[WARN] Statement {i}: Table doesn't exist (ignoring)")
                elif 'already exists' in error_msg.lower():
                    print(f"[WARN] Statement {i}: Object already exists (ignoring)")
                else:
                    print(f"[ERROR] Statement {i}: {e}")
                    print(f"   First 100 chars: {stmt[:100]}...")

        cursor.close()
        conn.close()
        print(f"\n[OK] {filename} completed successfully")
        return True

    except Exception as e:
        print(f"\n[ERROR] Error executing {filename}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main execution function."""
    print("Oracle Database Setup Script")
    print("="*60)
    print(f"Connecting to: {settings.connection_string}")
    print(f"User: {settings.DB_USER}")

    # Execute scripts in order
    scripts = [
        '01_create_schema.sql',
        '02_create_tables.sql',
        '03_seed_sample_data.sql',
        '05_plsql_objects.sql'
    ]

    for script in scripts:
        if not execute_sql_file(script):
            print(f"\n[ERROR] Failed at {script}. Stopping.")
            return

    print("\n" + "="*60)
    print("[OK] All scripts executed successfully!")
    print("="*60)


if __name__ == "__main__":
    main()
