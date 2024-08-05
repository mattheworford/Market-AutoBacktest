import os
import sys
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


from config.config import (
    POLY_API_KEY,
    POLY_BASE_URL,
    POLY_SYMBOL,
    POLY_MULTIPLIER,
    POLY_TIMESPAN,
    POLY_FROM_,
    POLY_TO,
)

from client.polygon import PolygonApiClient
from services.polygon_services import PolygonDataService
from utils.api_constructor_utils import PolygonApiConstructor
from models.polygon_models.polygon_previous_close import PolygonDailyApiResponse
from models.polygon_models.polygon_aggregate_bars import PolygonAggregatesResponse
from typing import Callable


def main() -> None:
    assert POLY_API_KEY is not None  # Type assertion for mypy
    try:
        # Instantiate all classes
        daily_client = PolygonApiClient(key=POLY_API_KEY, base_url=POLY_BASE_URL)
        poly_data_service = PolygonDataService(api_client=daily_client)
        poly_api_constructor = PolygonApiConstructor(base_url=POLY_BASE_URL)

        # Use the daily endpoint
        poly_endpoint_constructor: Callable[[str, str], str] = (
            poly_api_constructor.construct_previous_close_endpoint
        )
        poly_data = poly_data_service.fetch_data_with_endpoint(
            poly_endpoint_constructor,
            PolygonDailyApiResponse,
            api_key=POLY_API_KEY,
            symbol=POLY_SYMBOL,
        )
        print(poly_data.to_json(indent=4))

        # Use aggregate endpoint
        poly_endpoint_constructor_agg: Callable[[str, str, int, str, str, str], str] = (
            poly_api_constructor.construct_aggregate_bars_endpoint
        )
        poly_data = poly_data_service.fetch_data_with_endpoint(
            poly_endpoint_constructor_agg,
            PolygonAggregatesResponse,
            api_key=POLY_API_KEY,
            symbol=POLY_SYMBOL,
            multiplier=POLY_MULTIPLIER,
            timespan=POLY_TIMESPAN,
            from_=POLY_FROM_,
            to=POLY_TO,
        )
        print(poly_data.to_json(indent=4))

    except Exception as e:
        raise Exception(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
