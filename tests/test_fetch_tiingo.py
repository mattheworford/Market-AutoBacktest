from typing import Generator
import pytest
import os
from unittest.mock import patch, MagicMock
import pandas as pd
from data_ingestion import fetch_tiingo_data


@pytest.fixture
def mock_env_var() -> Generator[None, None, None]:
    with patch.dict(os.environ, {"TIINGO_API_KEY": "test_api_key"}):
        yield


@pytest.fixture
def mock_requests_get() -> Generator[MagicMock, None, None]:
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.text = '[{"date": "2020-01-01", "open": 100, "close": 110}, {"date": "2020-01-02", "open": 101, "close": 111}]'
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        yield mock_get


def test_fetch_tiingo_data(
    mock_env_var: Generator[None, None, None],
    mock_requests_get: MagicMock,
) -> None:
    symbol = "AAPL"
    start_date = "2020-01-01"
    end_date = "2020-01-02"

    result = fetch_tiingo_data(symbol, start_date, end_date)

    mock_requests_get.assert_called_once_with(
        f"https://api.tiingo.com/tiingo/daily/{symbol}/prices",
        params={
            "startDate": start_date,
            "endDate": end_date,
            "token": "test_api_key",
        },
    )
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert list(result.columns) == ["date", "open", "close"]
