from typing import Generator
import pytest
import os
from unittest.mock import patch, MagicMock
import pandas as pd
from config.config import MARKET_DATA_COLUMNS
from data_ingestion import fetch_tiingo_data


@pytest.fixture
def mock_env_var() -> Generator[None, None, None]:
    with patch.dict(os.environ, {"TIINGO_API_KEY": "test_api_key"}):
        yield


@pytest.fixture
def mock_requests_get() -> Generator[MagicMock, None, None]:
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.text = """[
            {
                "date": "2023-01-01T00:00:00.000Z",
                "open": 150.0,
                "high": 155.0,
                "low": 148.0,
                "close": 154.0,
                "volume": 1000000,
                "adjClose": 153.0,
                "adjHigh": 154.0,
                "adjLow": 147.0,
                "adjOpen": 149.0,
                "adjVolume": 950000,
                "divCash": 0.0,
                "splitFactor": 1.0
            },
            {
                "date": "2023-01-02T00:00:00.000Z",
                "open": 152.0,
                "high": 157.0,
                "low": 150.0,
                "close": 156.0,
                "volume": 1200000,
                "adjClose": 155.0,
                "adjHigh": 156.0,
                "adjLow": 149.0,
                "adjOpen": 151.0,
                "adjVolume": 1150000,
                "divCash": 0.0,
                "splitFactor": 1.0
            },
            {
                "date": "2023-01-03T00:00:00.000Z",
                "open": 155.0,
                "high": 160.0,
                "low": 153.0,
                "close": 158.0,
                "volume": 1100000,
                "adjClose": 157.0,
                "adjHigh": 159.0,
                "adjLow": 152.0,
                "adjOpen": 154.0,
                "adjVolume": 1050000,
                "divCash": 0.0,
                "splitFactor": 1.0
            }
        ]"""
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
    assert list(result.columns) == [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "ex_dividend",
        "split_ratio",
        "adjusted_open",
        "adjusted_high",
        "adjusted_low",
        "adjusted_close",
        "adjusted_volume",
    ]
