from dotenv import load_dotenv
from typing import Optional

# Load environment variables from a .env file
load_dotenv()

from config.config import AV_API_KEY, BASE_URL, SYMBOL, OUTPUT
from client.alpha_vantage import AlphaVantageApiClient
from services.alpha_vantage_services import AlphaVantanageDataService
from utils.api_constructor_utils import AlphaVantageApiConstructor
from models.alpha_vantage_models.alpha_vantage_daily import AlphaVantageResponse


def fetch_av_timeseries_daily_data() -> str:
    assert AV_API_KEY is not None  # Type assertion for mypy

    client = AlphaVantageApiClient(key=AV_API_KEY, base_url=BASE_URL)
    data_service = AlphaVantanageDataService(api_client=client)
    api_constructor = AlphaVantageApiConstructor(base_url=BASE_URL)

    endpoint_constructor = api_constructor.construct_time_series_daily_endpoint
    data = data_service.fetch_data_with_endpoint(
        endpoint_constructor,
        AlphaVantageResponse,
        symbol=SYMBOL,
        api_key=AV_API_KEY,
        output=OUTPUT,
    )
    return data_service.get_json_response(data)
