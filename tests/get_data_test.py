import pytest
from unittest.mock import patch, Mock
import json
from client.alpha_vantage import AlphaVantageApiClient
from models.alpha_vantage_models.alpha_vantage_daily import AlphaVantageResponse
from typing import Generator


@pytest.fixture
def mock_get() -> Generator[Mock, None, None]:
    with patch("client.alpha_vantage.requests.get") as mock_get:
        yield mock_get


def test_get_data(mock_get: Mock) -> None:
    # Mock response data
    mock_response = Mock()
    expected_data = {
        "Meta Data": {
            "1. Information": "Daily Prices (open, high, low, close) and Volumes",
            "2. Symbol": "IBM",
            "3. Last Refreshed": "2024-08-02",
            "4. Output Size": "Compact",
            "5. Time Zone": "US/Eastern",
        },
        "Time Series (Daily)": {
            "2024-08-02": {
                "1. open": "188.7800",
                "2. high": "189.2600",
                "3. low": "185.7000",
                "4. close": "189.1200",
                "5. volume": "4548824",
            }
        },
    }
    mock_response.json.return_value = expected_data
    mock_response.text = json.dumps(expected_data)
    mock_get.return_value = mock_response

    client = AlphaVantageApiClient(
        key="fake_api_key", base_url="https://www.alphavantage.co/query"
    )
    result = client.get_data(
        lambda symbol, api_key: f"?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}",
        AlphaVantageResponse,
        symbol="IBM",
        api_key="fake_api_key",
    )

    assert result.meta_data.symbol == "IBM"
    assert result.time_series_daily["2024-08-02"].open == "188.7800"