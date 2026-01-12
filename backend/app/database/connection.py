from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
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
db_url = convert_postgres_to_asyncpg_url(settings.database_url)

# Async engine for FastAPI with Neon-specific settings
async_engine = create_async_engine(
    db_url,
    echo=True,  # Set to False in production
    connect_args={"ssl": "require"},
    pool_size=5,  # Neon recommends smaller pool sizes
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300  # Recycle connections periodically
)

# Async session factory
async_session = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

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