"""Application configuration using environment variables."""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # PostgreSQL/Neon Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # Legacy Oracle Configuration (kept for reference)
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "1521")
    DB_SERVICE: str = os.getenv("DB_SERVICE", "FREEPDB1")
    DB_USER: str = os.getenv("DB_USER", "hr_app")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")

    @property
    def connection_string(self) -> str:
        """Construct connection string (for PostgreSQL)."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        # Fallback to legacy format
        return f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_SERVICE}"


settings = Settings()
