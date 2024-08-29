import pytest
from unittest.mock import Mock, patch
from sqlalchemy.exc import SQLAlchemyError
import os
from typing import Generator
import logging


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("INSTANCE_CONNECTION_NAME", "=testid:us-central1:testdb")
    monkeypatch.setenv("DB_USER", "test_user")
    monkeypatch.setenv("DB_PASS", "test_pass")
    monkeypatch.setenv("DB_NAME", "test_db")


from test_db_connection import test_connection


@pytest.fixture
def mock_db_connection() -> Generator[Mock, None, None]:
    with patch("test_db_connection.db.connect") as mock_connect:
        mock_conn = Mock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        yield mock_conn


@pytest.fixture(autouse=True)
def setup_logging(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)


def test_successful_connection(
    mock_db_connection: Mock, caplog: pytest.LogCaptureFixture
) -> None:
    # Mock successful database operations
    mock_db_connection.execute.side_effect = [
        Mock(scalar=lambda: "test_db"),
        Mock(scalar=lambda: "PostgreSQL 13.0"),
        None,
        None,
        Mock(fetchall=lambda: [("row1",), ("row2",)]),
        Mock(fetchall=lambda: [("table1",), ("table2",)]),
        Mock(fetchall=lambda: [("table1",), ("table2",)]),
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
    assert (
        "All tables in database after commit: [('table1',), ('table2',)]" in caplog.text
    )
    assert (
        "Query result from second_table after commit: [('row1',), ('row2',)]"
        in caplog.text
    )

    # Assert database operations were called
    assert mock_db_connection.execute.call_count == 8
    assert mock_db_connection.commit.call_count == 1


def test_connection_failure(
    mock_db_connection: Mock, caplog: pytest.LogCaptureFixture
) -> None:
    # Mock SQLAlchemyError
    mock_db_connection.execute.side_effect = SQLAlchemyError("Connection failed")

    test_connection()

    # Assert error log message
    assert "Connection failed. Error: Connection failed" in caplog.text


if __name__ == "__main__":
    pytest.main()
