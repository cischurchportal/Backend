"""
Database session management using SQLAlchemy with Azure SQL (pyodbc/pymssql).
Auto-creates and migrates tables on startup.
"""
import os
import logging
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker, Session

logger = logging.getLogger(__name__)

_engine = None
_SessionLocal = None


def get_engine():
    global _engine
    if _engine is None:
        server = os.getenv("AZURE_SQL_SERVER", "")
        database = os.getenv("AZURE_SQL_DATABASE", "")
        username = os.getenv("AZURE_SQL_USERNAME", "")
        password = os.getenv("AZURE_SQL_PASSWORD", "")
        port = os.getenv("AZURE_SQL_PORT", "1433")

        from urllib.parse import quote_plus
        import platform

        is_azure = os.getenv("WEBSITE_INSTANCE_ID") is not None
        is_linux = platform.system() == "Linux"

        if is_azure or is_linux:
            # Azure Functions Linux — ODBC Driver 18 is pre-installed
            conn_str = (
                f"mssql+pyodbc://{quote_plus(username)}:{quote_plus(password)}"
                f"@{server},{port}/{database}"
                f"?driver=ODBC+Driver+18+for+SQL+Server"
                f"&Encrypt=yes&TrustServerCertificate=no&Connection+Timeout=30"
            )
        else:
            # Local Windows dev — use pymssql (no driver install needed)
            conn_str = (
                f"mssql+pymssql://{quote_plus(username)}:{quote_plus(password)}"
                f"@{server}:{port}/{database}"
            )

        _engine = create_engine(
            conn_str,
            echo=False,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
        logger.info(f"SQLAlchemy engine created for Azure SQL: {server},{port}/{database}")
    return _engine


def get_session_factory():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=get_engine()
        )
    return _SessionLocal


def get_db() -> Session:
    """Dependency-style session getter. Use as context manager."""
    SessionLocal = get_session_factory()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Create all tables if they don't exist.
    For new columns added to existing tables, uses ALTER TABLE via inspect.
    """
    from app.db.models import Base
    engine = get_engine()

    logger.info("Initializing database schema...")
    # create_all with checkfirst=True creates missing tables without dropping existing ones
    Base.metadata.create_all(bind=engine, checkfirst=True)

    # Add any missing columns to existing tables (simple migration)
    _add_missing_columns(engine, Base)

    logger.info("Database schema initialized successfully")


def _add_missing_columns(engine, Base):
    """Add columns that exist in models but not yet in the DB (forward migration)."""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    for table in Base.metadata.sorted_tables:
        if table.name not in existing_tables:
            continue  # Will be created by create_all

        existing_cols = {col["name"] for col in inspector.get_columns(table.name)}

        for column in table.columns:
            if column.name not in existing_cols:
                col_type = column.type.compile(dialect=engine.dialect)
                nullable = "NULL" if column.nullable else "NOT NULL"
                default_clause = ""
                if column.default is not None and column.default.is_scalar:
                    val = column.default.arg
                    if isinstance(val, bool):
                        default_clause = f" DEFAULT {1 if val else 0}"
                    elif isinstance(val, (int, float)):
                        default_clause = f" DEFAULT {val}"
                    elif isinstance(val, str):
                        default_clause = f" DEFAULT '{val}'"

                alter_sql = (
                    f"ALTER TABLE {table.name} ADD {column.name} "
                    f"{col_type} {nullable}{default_clause}"
                )
                try:
                    with engine.connect() as conn:
                        conn.execute(text(alter_sql))
                        conn.commit()
                    logger.info(f"Added column {column.name} to {table.name}")
                except Exception as e:
                    logger.warning(f"Could not add column {column.name} to {table.name}: {e}")
