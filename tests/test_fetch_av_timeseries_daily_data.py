import pytest
from unittest.mock import MagicMock, patch, Mock
from client.alpha_vantage import AlphaVantageApiClient
from services.alpha_vantage_services import AlphaVantanageDataService
from utils.api_constructor_utils import AlphaVantageApiConstructor
from models.alpha_vantage_models.alpha_vantage_daily import (
    AlphaVantageResponse,
    MetaData,
    TimeSeriesDaily,
)
from data_ingestion.fetch_alpha_vantage import fetch_av_timeseries_daily_data
from typing import Any
import json


@patch("client.alpha_vantage.AlphaVantageApiClient.get_data")
@patch("data_ingestion.fetch_alpha_vantage.AlphaVantageApiClient")
@patch("data_ingestion.fetch_alpha_vantage.AlphaVantanageDataService")
@patch("data_ingestion.fetch_alpha_vantage.AlphaVantageApiConstructor")
def test_fetch_av_timeseries_daily_data(
    mock_constructor: Any, mock_service: Any, mock_client: Any, mock_get_data: Any
) -> None:
    # Mock response data
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

    # Create a mock response object with the JSON content
    mock_response = Mock()
    mock_response.json.return_value = expected_data
    mock_response.text = json.dumps(expected_data)
    mock_get_data.return_value = AlphaVantageResponse.from_dict(expected_data)

    mock_constructor.return_value.construct_time_series_daily_endpoint = MagicMock(
        return_value="mock_endpoint"
    )
    mock_service.return_value.fetch_data_with_endpoint.return_value = (
        AlphaVantageResponse.from_dict(expected_data)
    )
    mock_service.return_value.get_json_response.return_value = json.dumps(
        expected_data, indent=4
    )

    result = fetch_av_timeseries_daily_data()

    expected_response = AlphaVantageResponse(
        meta_data=MetaData(
            information="Daily Prices (open, high, low, close) and Volumes",
            symbol="IBM",
            last_refreshed="2024-08-02",
            output_size="Compact",
            time_zone="US/Eastern",
        ),
        time_series_daily={
            "2024-08-02": TimeSeriesDaily(
                open="188.7800",
                high="189.2600",
                low="185.7000",
                close="189.1200",
                volume="4548824",
            )
        },
    )

    assert json.loads(result) == json.loads(expected_response.to_json(indent=4))
