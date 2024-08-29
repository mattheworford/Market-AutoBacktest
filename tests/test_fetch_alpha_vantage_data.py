from typing import Generator
import pytest
import os
from unittest.mock import patch, MagicMock
import pandas as pd
from data_ingestion.fetch_alpha_vantage import (
    fetch_alpha_vantage_data,
    standardize_data,
)


@pytest.fixture
def mock_env_vars() -> Generator[None, None, None]:
    with patch.dict(os.environ, {"AV_API_KEY": "test_key"}):
        yield


@pytest.fixture
def mock_alpha_vantage_response() -> dict[str, dict[str, dict[str, str]]]:
    return {
        "Time Series (Daily)": {
            "2024-08-12": {
                "1. open": "534.2100",
                "2. high": "535.7300",
                "3. low": "530.9500",
                "4. close": "533.2700",
                "5. volume": "42542069",
            },
            "2024-08-09": {
                "1. open": "529.8100",
                "2. high": "534.5100",
                "3. low": "528.5600",
                "4. close": "532.9900",
                "5. volume": "45619558",
            },
        }
    }


@patch("data_ingestion.fetch_alpha_vantage.requests.get")
def test_fetch_alpha_vantage_data(
    mock_get: MagicMock,
    mock_alpha_vantage_response: dict[str, dict[str, dict[str, str]]],
    mock_env_vars: None,
) -> None:
    mock_get.return_value.json.return_value = mock_alpha_vantage_response
    mock_get.return_value.raise_for_status = MagicMock()

    # Fetch the data
    df = fetch_alpha_vantage_data(symbol="SPY", output="full")

    # Standardize the data (if not done in the fetch function)
    standardized_df = standardize_data(df)

    # Now assert using the standardized DataFrame
    assert not standardized_df.empty
    assert standardized_df.index[0] == pd.to_datetime("2024-08-12")
    assert standardized_df.iloc[0]["open"] == "534.2100"
    assert standardized_df.iloc[0]["high"] == "535.7300"
    assert standardized_df.iloc[0]["low"] == "530.9500"
    assert standardized_df.iloc[0]["close"] == "533.2700"
    assert standardized_df.iloc[0]["volume"] == "42542069"


def test_standardize_data(
    mock_alpha_vantage_response: dict[str, dict[str, dict[str, str]]]
) -> None:
    time_series = mock_alpha_vantage_response.get("Time Series (Daily)", {})
    df = pd.DataFrame.from_dict(time_series, orient="index")

    standardized_df = standardize_data(df)

    assert not standardized_df.empty
    assert standardized_df.index[0] == pd.to_datetime("2024-08-12")
    assert standardized_df.iloc[0]["open"] == "534.2100"
    assert standardized_df.iloc[0]["high"] == "535.7300"
    assert standardized_df.iloc[0]["low"] == "530.9500"
    assert standardized_df.iloc[0]["close"] == "533.2700"
    assert standardized_df.iloc[0]["volume"] == "42542069"
