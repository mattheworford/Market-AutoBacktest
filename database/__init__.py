import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sqlalchemy.engine.base

load_dotenv()


def init_connection_engine() -> sqlalchemy.engine.base.Engine:
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_name = os.getenv("DB_NAME")

    print(f"Debug: DB_USER = {db_user}")
    print(f"Debug: DB_PASS = {'*' * len(db_pass) if db_pass else None}")
    print(f"Debug: DB_NAME = {db_name}")

    if not all([db_user, db_pass, db_name]):
        raise ValueError("Missing required environment variables")

    engine = create_engine(
        f"postgresql://{db_user}:{db_pass}@localhost:5433/{db_name}",
        echo=True,  # This will log all SQL statements
        isolation_level="AUTOCOMMIT",  # This will ensure transactions are committed immediately
    )
    return engine


db = init_connection_engine()

__all__ = ["db"]
