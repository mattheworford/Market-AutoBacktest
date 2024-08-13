from typing import Generator
import pytest
import os
from unittest.mock import patch, MagicMock
import pandas as pd
from config.config import MARKET_DATA_COLUMNS
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
                "Date": ["2023-01-01", "2023-01-02", "2023-01-03"],
                "Open": [149.0, 151.0, 153.0],
                "High": [154.0, 156.0, 158.0],
                "Low": [147.0, 149.0, 151.0],
                "Close": [153.0, 155.0, 157.0],
                "Volume": [1100000, 1300000, 1200000],
                "Ex-Dividend": [0.0, 0.0, 0.0],
                "Split Ratio": [1.0, 1.0, 1.0],
                "Adj. Open": [148.0, 150.0, 152.0],
                "Adj. High": [153.0, 155.0, 157.0],
                "Adj. Low": [146.0, 148.0, 150.0],
                "Adj. Close": [152.0, 154.0, 156.0],
                "Adj. Volume": [1050000, 1250000, 1150000],
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
