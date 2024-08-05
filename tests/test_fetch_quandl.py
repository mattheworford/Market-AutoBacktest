from typing import Generator
import pytest
from io import StringIO
from unittest.mock import MagicMock, patch
from config.config import QUANDL_API_KEY
from data_ingestion import fetch_quandl_data
import os
from dotenv import load_dotenv


@pytest.fixture
def mock_get(monkeypatch: pytest.MonkeyPatch) -> Generator[MagicMock, None, None]:
    with patch("requests.get") as mock_get:
        yield mock_get


@pytest.fixture
def mock_read_csv(monkeypatch: pytest.MonkeyPatch) -> Generator[MagicMock, None, None]:
    with patch("pandas.read_csv") as mock_read_csv:
        yield mock_read_csv


def test_fetch_quandl_data(mock_read_csv: MagicMock, mock_get: MagicMock) -> None:
    load_dotenv(verbose=False)
    QUANDL_API_KEY = os.getenv("QUANDL_API_KEY")

    mock_response = mock_get.return_value
    mock_response.text = "Date,Open,High,Low,Close,Volume,Ex-Dividend,Split Ratio,Adj. Open,Adj. High,Adj. Low,Adj. Close,Adj. Volume\n2020-01-01,100.0,105.0,95.0,102.0,1000000,0.0,1.0,100.0,105.0,95.0,102.0,1000000\n"
    mock_csv_data = StringIO(mock_response.text)
    mock_response.status_code = 200
    mock_data = mock_read_csv.return_value

    data = fetch_quandl_data("AAPL", start_date="2020-01-01", end_date="2020-01-02")

    mock_get.assert_called_once_with(
        "https://www.quandl.com/api/v3/datasets/WIKI/AAPL.csv",
        params={
            "start_date": "2020-01-01",
            "end_date": "2020-01-02",
            "api_key": QUANDL_API_KEY,
        },
    )
    actual_call_arg = mock_read_csv.call_args[0][0]
    assert actual_call_arg.getvalue() == mock_csv_data.getvalue()
    assert data == mock_data
