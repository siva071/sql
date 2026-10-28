"""Test Neon PostgreSQL connection."""
import psycopg2
from config.settings import settings

print("Testing Neon PostgreSQL Connection")
print("="*60)
print(f"Database URL: {settings.DATABASE_URL[:30]}...")

try:
    conn = psycopg2.connect(settings.DATABASE_URL)
    print("[OK] Connection successful!")
    conn.close()
except Exception as e:
    print(f"[ERROR] Connection failed: {e}")
