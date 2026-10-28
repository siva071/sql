"""Script to execute PostgreSQL setup files using psycopg2."""
import psycopg2
from config.settings import settings
import os


def execute_sql_file(filename):
    """Execute a SQL file."""
    filepath = os.path.join('sql', filename)
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return False

    print(f"\n{'='*60}")
    print(f"Executing: {filename}")
    print('='*60)

    try:
        conn = psycopg2.connect(settings.DATABASE_URL)
        cursor = conn.cursor()

        with open(filepath, 'r') as f:
            sql_content = f.read()

        # For PostgreSQL, execute the entire file as-is for functions
        # PostgreSQL handles multiple statements in functions with $$ strings
        cursor.execute(sql_content)
        conn.commit()

        print(f"[OK] {filename} completed successfully")
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        error_msg = str(e)
        if 'already exists' in error_msg.lower():
            print(f"[WARN] {filename}: Object already exists (ignoring)")
            return True
        else:
            print(f"[ERROR] Error executing {filename}: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main execution function."""
    print("PostgreSQL Database Setup Script")
    print("="*60)
    print(f"Connecting to Neon PostgreSQL")
    print(f"Database URL: {settings.DATABASE_URL[:30]}...")

    # Execute scripts in order
    scripts = [
        '01_create_schema_postgres.sql',
        '02_seed_sample_data_postgres.sql',
        '03_plsql_objects_postgres.sql'
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
