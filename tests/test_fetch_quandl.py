from typing import Generator
import pytest
import os
from unittest.mock import patch, MagicMock
import pandas as pd
from data_ingestion import fetch_quandl_data


@pytest.fixture
def mock_env_var() -> Generator[None, None, None]:
    with patch.dict(os.environ, {"QUANDL_API_KEY": "test_api_key"}):
        yield


@pytest.fixture
def mock_nasdaqdatalink_get() -> Generator[MagicMock, None, None]:
    with patch("nasdaqdatalink.get") as mock_get:
        mock_df = pd.DataFrame(
            {
                "Date": ["2018-01-01", "2018-01-02"],
                "Open": [100, 101],
                "Close": [110, 111],
            }
        )
        mock_get.return_value = mock_df
        yield mock_get


def test_fetch_quandl_data(
    mock_env_var: Generator[None, None, None],
    mock_nasdaqdatalink_get: MagicMock,
) -> None:
    symbol = "AAPL"
    start_date = "2018-01-01"
    end_date = "2018-01-02"

    result: pd.DataFrame = fetch_quandl_data(symbol, start_date, end_date)

    mock_nasdaqdatalink_get.assert_called_once_with(
        f"WIKI/{symbol}",
        start_date=start_date,
        end_date=end_date,
    )
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert list(result.columns) == ["Date", "Open", "Close"]
