import os
from typing import Callable
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


def fetch_polygon_previous_close() -> PolygonDailyApiResponse:
    assert POLY_API_KEY is not None  # Type assertion for mypy

    client = PolygonApiClient(key=POLY_API_KEY, base_url=POLY_BASE_URL)
    data_service = PolygonDataService(api_client=client)
    api_constructor = PolygonApiConstructor(base_url=POLY_BASE_URL)

    endpoint_constructor: Callable[[str, str], str] = (
        api_constructor.construct_previous_close_endpoint
    )
    data = data_service.fetch_data_with_endpoint(
        endpoint_constructor,
        PolygonDailyApiResponse,
        api_key=POLY_API_KEY,
        symbol=POLY_SYMBOL,
    )
    return data


def fetch_polygon_agg_bars() -> PolygonAggregatesResponse:
    if POLY_API_KEY is None:
        raise ValueError("POLY_API_KEY cannot be None")

    client = PolygonApiClient(key=POLY_API_KEY, base_url=POLY_BASE_URL)
    data_service = PolygonDataService(api_client=client)
    api_constructor = PolygonApiConstructor(base_url=POLY_BASE_URL)

    endpoint_constructor: Callable[[str, str, int, str, str, str], str] = (
        api_constructor.construct_aggregate_bars_endpoint
    )
    data = data_service.fetch_data_with_endpoint(
        endpoint_constructor,
        PolygonAggregatesResponse,
        api_key=POLY_API_KEY,
        symbol=POLY_SYMBOL,
        multiplier=POLY_MULTIPLIER,
        timespan=POLY_TIMESPAN,
        from_=POLY_FROM_,
        to=POLY_TO,
    )
    return data
