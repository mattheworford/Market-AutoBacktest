import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError
import os
from typing import Generator
import logging
from sqlalchemy.engine.base import Engine, Connection

# Import test_connection at the top level
from db_connection import test_connection


@pytest.fixture
def mock_env_vars() -> Generator[None, None, None]:
    with patch.dict(
        os.environ,
        {
            "DB_USER": "test_user",
            "DB_PASS": "test_pass",
            "DB_NAME": "test_db",
            "INSTANCE_CONNECTION_NAME": "testid:us-central1:testdb",
        },
    ):
        yield


@pytest.fixture
def mock_db_connection() -> Generator[Mock, None, None]:
    mock_conn = Mock(spec=Connection)
    yield mock_conn


@pytest.fixture(autouse=True)
def setup_logging(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)


@patch("db_connection.db.connect")
def test_successful_connection(
    mock_connect: Mock,
    mock_db_connection: Mock,
    caplog: pytest.LogCaptureFixture,
    mock_env_vars: None,
) -> None:
    mock_connect.return_value.__enter__.return_value = mock_db_connection
    # Mock successful database operations
    mock_db_connection.execute.side_effect = [
        Mock(scalar=lambda: "test_db"),
        Mock(scalar=lambda: "PostgreSQL 13.0"),
        None,
        None,
        Mock(fetchall=lambda: [("row1",), ("row2",)]),
        Mock(fetchall=lambda: [("table1",), ("table2",)]),
        None,  # For the DELETE operation
        Mock(fetchall=lambda: [("row1",), ("row2",)]),
    ]

    test_connection()

    # Assert log messages
    assert "Connected to database" in caplog.text
    assert "Current database: test_db" in caplog.text
    assert "PostgreSQL version: PostgreSQL 13.0" in caplog.text
    assert "second_table created or already exists" in caplog.text
    assert "Data 'wcs' inserted into second_table" in caplog.text
    assert "Query result from second_table: [('row1',), ('row2',)]" in caplog.text
    assert "All tables in database: [('table1',), ('table2',)]" in caplog.text
    assert "Data 'wcs' deleted from second_table" in caplog.text
    assert (
        "Query result from second_table after cleanup: [('row1',), ('row2',)]"
        in caplog.text
    )

    # Assert database operations were called
    assert mock_db_connection.execute.call_count == 8
    assert mock_db_connection.commit.call_count == 2


@patch("db_connection.db.connect")
def test_connection_failure(
    mock_connect: Mock,
    mock_db_connection: Mock,
    caplog: pytest.LogCaptureFixture,
    mock_env_vars: None,
) -> None:
    mock_connect.return_value.__enter__.return_value = mock_db_connection
    # Mock SQLAlchemyError
    mock_db_connection.execute.side_effect = SQLAlchemyError("Connection failed")

    test_connection()

    # Assert error log message
    assert "Connection failed. Error: Connection failed" in caplog.text


if __name__ == "__main__":
    pytest.main()
