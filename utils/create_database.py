from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
import logging

logger = logging.getLogger(__name__)

def create_database(database_url, database_name):
    engine = create_engine(database_url)
    conn = engine.connect()
    conn.execution_options(isolation_level="AUTOCOMMIT")
    
    try:
        conn.execute(text(f"CREATE DATABASE {database_name}"))
        logger.info(f"Database '{database_name}' created successfully.")
    except ProgrammingError as e:
        if 'already exists' in str(e):
            logger.info(f"Database '{database_name}' already exists.")
        else:
            logger.error(f"Error creating database '{database_name}': {str(e)}")
    finally:
        conn.close()
