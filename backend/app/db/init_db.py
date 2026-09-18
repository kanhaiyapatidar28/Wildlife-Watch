"""Database initialization module to set up PostGIS extensions and create tables."""
import logging
from sqlalchemy import text
from app.db.session import engine
from app.db.base import Base
# Import all models so that Base.metadata has full registry
import app.models  # noqa: F401

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wildlife_watch.init_db")


def init_db(check_postgis: bool = True) -> bool:
    """Initialize database extensions and schema tables."""
    try:
        with engine.connect() as connection:
            logger.info("Connecting to database at %s...", engine.url.render_as_string(hide_password=True))
            if check_postgis:
                try:
                    logger.info("Attempting to enable PostGIS extension...")
                    connection.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
                    connection.commit()
                    logger.info("PostGIS extension verified successfully.")
                except Exception as ext_err:
                    logger.warning("Could not enable PostGIS extension (may not have SUPERUSER or not running PostgreSQL): %s", ext_err)

            logger.info("Creating all registered database tables from Base.metadata...")
            Base.metadata.create_all(bind=connection)
            connection.commit()
            logger.info("Database tables successfully created: %s", list(Base.metadata.tables.keys()))
            return True
    except Exception as e:
        logger.error("Failed to initialize database: %s", e)
        return False


if __name__ == "__main__":
    success = init_db()
    if success:
        print("Database initialization complete.")
    else:
        print("Database initialization encountered errors.")
