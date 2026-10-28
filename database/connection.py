"""PostgreSQL database connection management using psycopg2 with retry logic."""
import logging
import psycopg2
from config.settings import settings
from contextlib import contextmanager
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Manages PostgreSQL database connections with retry logic."""

    def __init__(self):
        """Initialize database connection manager."""
        pass

    @contextmanager
    def get_connection(self, max_retries=3, retry_delay=1):
        """
        Get a database connection as a context manager with retry logic.

        Args:
            max_retries: Maximum number of connection retry attempts
            retry_delay: Delay between retries in seconds

        Yields:
            psycopg2.extensions.connection: Active database connection
        """
        conn = None
        for attempt in range(max_retries):
            try:
                # Use DATABASE_URL if available, otherwise build from components
                if settings.DATABASE_URL:
                    conn = psycopg2.connect(settings.DATABASE_URL)
                else:
                    # Fallback to individual parameters
                    conn = psycopg2.connect(
                        host=settings.DB_HOST,
                        port=settings.DB_PORT,
                        database=settings.DB_SERVICE,
                        user=settings.DB_USER,
                        password=settings.DB_PASSWORD
                    )
                logger.info("Database connection established successfully")
                yield conn
                return
            except psycopg2.Error as e:
                if conn:
                    try:
                        conn.close()
                    except:
                        pass

                if attempt < max_retries - 1:
                    logger.warning(f"Connection attempt {attempt + 1} failed, retrying in {retry_delay}s... Error: {e}")
                    time.sleep(retry_delay)
                else:
                    logger.error(f"Database connection failed after {max_retries} attempts: {e}")
                    raise Exception(
                        f"Cannot connect to PostgreSQL Database. "
                        f"Error: {e}. "
                        f"Check your .env file and ensure PostgreSQL Database is running."
                    ) from e
            finally:
                if conn:
                    try:
                        conn.close()
                        logger.info("Database connection closed")
                    except psycopg2.Error as e:
                        logger.error(f"Error closing connection: {e}")


# Global connection instance
db_connection = DatabaseConnection()
