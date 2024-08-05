import pytest
from unittest.mock import patch, Mock
from services.alpha_vantage_services import AlphaVantanageDataService
from models.alpha_vantage_models.alpha_vantage_daily import AlphaVantageResponse
import json


@pytest.fixture
def mock_api_client():
    with patch(
        "services.alpha_vantage_services.AlphaVantageApiClient"
    ) as MockApiClient:
        yield MockApiClient


def test_fetch_and_transform_data(mock_api_client):
    # Mock client response
    mock_client = mock_api_client.return_value
    mock_client.get_data.return_value = AlphaVantageResponse(
        meta_data={
            "1. Information": "Daily Prices (open, high, low, close) and Volumes",
            "2. Symbol": "IBM",
            "3. Last Refreshed": "2024-08-02",
            "4. Output Size": "Compact",
            "5. Time Zone": "US/Eastern",
        },
        time_series_daily={},
    )

    service = AlphaVantanageDataService(api_client=mock_client)
    result = service.fetch_data_with_endpoint(
        lambda symbol, api_key: f"?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}",
        AlphaVantageResponse,
        symbol="IBM",
        api_key="fake_api_key",
    )

    assert result.meta_data["2. Symbol"] == "IBM"


def test_get_json_response():
    # Mock AlphaVantageResponse object
    mock_data = AlphaVantageResponse(
        meta_data={
            "1. Information": "Daily Prices (open, high, low, close) and Volumes",
            "2. Symbol": "IBM",
            "3. Last Refreshed": "2024-08-02",
            "4. Output Size": "Compact",
            "5. Time Zone": "US/Eastern",
        },
        time_series_daily={},
    )

    service = AlphaVantanageDataService(api_client=None)
    result = service.get_json_response(mock_data)

    expected_dict = {
        "Meta Data": {
            "1. Information": "Daily Prices (open, high, low, close) and Volumes",
            "2. Symbol": "IBM",
            "3. Last Refreshed": "2024-08-02",
            "4. Output Size": "Compact",
            "5. Time Zone": "US/Eastern",
        },
        "Time Series (Daily)": {},
    }
    result_dict = json.loads(result)
    assert result_dict == expected_dict
