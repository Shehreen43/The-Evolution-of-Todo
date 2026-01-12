from sqlmodel import SQLModel
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from app.config import settings
import urllib.parse

def create_db_and_tables():
    """Create database tables using a synchronous engine with Neon database."""
    # Use the Neon database URL from environment
    db_url = settings.database_url

    # Convert asyncpg URL to sync PostgreSQL URL for table creation
    if db_url.startswith("postgresql+asyncpg://"):
        sync_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
    elif db_url.startswith("postgresql://"):
        sync_url = db_url
    else:
        # If it's not a PostgreSQL URL, raise an error
        raise ValueError(f"Unsupported database URL: {db_url}. Only PostgreSQL is supported.")

    # Create synchronous engine for table creation
    sync_engine = create_engine(
        sync_url,
        # Use connection pooling appropriate for Neon Serverless
        poolclass=StaticPool,
        # Ensure SSL is required for Neon
        connect_args={"sslmode": "require"}
    )

    # Create all tables defined in SQLModel models
    SQLModel.metadata.create_all(sync_engine)

def get_sync_engine():
    """Get a synchronous engine for operations that require it."""
    db_url = settings.database_url
    if db_url.startswith("postgresql+asyncpg://"):
        sync_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
    elif db_url.startswith("postgresql://"):
        sync_url = db_url
    else:
        sync_url = db_url

    return create_engine(
        sync_url,
        poolclass=StaticPool,
        connect_args={
            "prepared_statement_cache_size": 0,
        }
    )