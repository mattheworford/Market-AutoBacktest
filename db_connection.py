import logging
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from database import db

logging.basicConfig(level=logging.DEBUG)


def test_connection() -> None:
    try:
        with db.connect() as conn:
            logging.info("Connected to database")

            result = conn.execute(text("SELECT current_database()"))
            current_db = result.scalar()
            logging.info(f"Current database: {current_db}")

            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            logging.info(f"PostgreSQL version: {version}")

            # Create second_table
            conn.execute(
                text(
                    "CREATE TABLE IF NOT EXISTS second_table (id serial PRIMARY KEY, name VARCHAR(100))"
                )
            )
            logging.info("second_table created or already exists")

            # Insert 'wcs' into second_table
            conn.execute(text("INSERT INTO second_table (name) VALUES ('wcs')"))
            logging.info("Data 'wcs' inserted into second_table")

            # Query second_table
            query_result = conn.execute(text("SELECT * FROM second_table")).fetchall()
            logging.info(f"Query result from second_table: {query_result}")

            # List all tables
            tables = conn.execute(
                text(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
                )
            ).fetchall()
            logging.info(f"All tables in database: {tables}")

            # Commit the transaction explicitly
            conn.commit()

            # Clean up: Delete the inserted data
            conn.execute(text("DELETE FROM second_table WHERE name = 'wcs'"))
            logging.info("Data 'wcs' deleted from second_table")

            # Verify deletion
            query_result = conn.execute(text("SELECT * FROM second_table")).fetchall()
            logging.info(
                f"Query result from second_table after cleanup: {query_result}"
            )

            # Commit the cleanup
            conn.commit()

    except SQLAlchemyError as e:
        logging.error(f"Connection failed. Error: {str(e)}")


if __name__ == "__main__":
    test_connection()
