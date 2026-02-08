from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import text
from typing import Generator
from app.config import settings
import urllib.parse

def convert_postgres_to_asyncpg_url(postgres_url: str) -> str:
    """
    Convert a PostgreSQL URL to asyncpg format, handling query parameters properly for Neon.
    """
    parsed = urllib.parse.urlparse(postgres_url)

    # Check if it's already an asyncpg URL
    if parsed.scheme == 'postgresql+asyncpg':
        return postgres_url

    # Convert scheme
    if parsed.scheme in ['postgresql', 'postgres']:
        new_scheme = 'postgresql+asyncpg'
    else:
        return postgres_url  # Return as is if not postgres

    # Reconstruct URL with asyncpg scheme
    new_url = f"{new_scheme}://{parsed.netloc}{parsed.path}"

    # Handle query parameters - some need to be removed for Neon compatibility
    if parsed.query:
        # Parse query parameters
        query_params = urllib.parse.parse_qs(parsed.query)

        # Process parameters for asyncpg/Neon compatibility
        filtered_params = {}
        for key, values in query_params.items():
            value = values[0] if values else ''

            # Skip parameters that cause issues with Neon/asyncpg
            if key in ['channel_binding', 'gssencmode', 'krbsrvname', 'target_session_attrs']:
                continue
            # Keep important parameters like sslmode, but ensure proper format
            elif key == 'sslmode':
                continue
            elif key in ['sslcert', 'sslkey', 'sslrootcert', 'sslcrl',
                         'ssl_min_protocol_version', 'ssl_max_protocol_version']:
                continue
            else:
                # Include other parameters that don't cause issues
                filtered_params[key] = value

        if filtered_params:
            new_query = urllib.parse.urlencode(filtered_params, doseq=True)
            new_url += f"?{new_query}"

    return new_url

# Convert the database URL to asyncpg format for Neon
async_db_url = convert_postgres_to_asyncpg_url(settings.database_url)

# Determine if SSL is required based on DATABASE_URL or environment
# For local Docker Postgres, we typically don't use SSL
ssl_required = "sslmode=require" in settings.database_url or "neon.tech" in settings.database_url
connect_args = {"ssl": "require"} if ssl_required else {}

# Async engine for FastAPI with Neon-specific settings
async_engine = create_async_engine(
    async_db_url,
    echo=True,  # Set to False in production
    connect_args=connect_args,
    pool_size=5,  # Neon recommends smaller pool sizes
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300  # Recycle connections periodically
)

# Sync engine for MCP tools and other sync operations
sync_db_url = async_db_url.replace("postgresql+asyncpg://", "postgresql://")
sync_engine = create_engine(
    sync_db_url,
    echo=False,  # Set to True for SQL query logging during development
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
)

# Async session factory
async_session = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

from contextlib import contextmanager

@contextmanager
def get_session() -> Generator:
    """
    Dependency for getting synchronous SQLModel session.
    Used by advanced task routes.
    """
    with Session(sync_engine) as session:
        yield session

def get_sync_session() -> Generator:
    """
    Dependency function for providing synchronous database sessions.
    Used primarily for MCP tools and other sync operations.
    """
    with sync_engine.connect() as connection:
        with sync_engine.begin() as transaction:
            try:
                yield connection
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                raise

async def get_db():
    """Dependency for getting async database session."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    """Initialize database tables."""
    async with async_engine.begin() as conn:
        # Use run_sync to run the sync operation in an async context
        await conn.run_sync(SQLModel.metadata.create_all)

def init_sync_db():
    """Initialize database tables using sync engine."""
    SQLModel.metadata.create_all(sync_engine)

def check_db_connection() -> bool:
    """
    Check if database connection is working.

    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        with sync_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False