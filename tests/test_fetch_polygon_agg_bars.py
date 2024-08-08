import pytest
from unittest.mock import MagicMock, patch
from client.polygon import PolygonApiClient
from services.polygon_services import PolygonDataService
from utils.api_constructor_utils import PolygonApiConstructor
from models.polygon_models.polygon_aggregate_bars import (
    PolygonAggregatesResponse,
    AggResult,
)
from data_ingestion.fetch_polygon import fetch_polygon_agg_bars
from typing import Any


@patch.dict("os.environ", {"POLY_API_KEY": "fake_poly_api_key"})
@patch("client.polygon.PolygonApiClient.get_data")
@patch("data_ingestion.fetch_polygon.PolygonApiClient")
@patch("data_ingestion.fetch_polygon.PolygonDataService")
@patch("data_ingestion.fetch_polygon.PolygonApiConstructor")
def test_fetch_polygon_agg_bars(
    mock_constructor: Any, mock_service: Any, mock_client: Any, mock_get_data: Any
) -> None:
    mock_response = PolygonAggregatesResponse(
        adjusted=True,
        queryCount=1,
        request_id="mock_request_id",
        results=[
            AggResult(
                c=209.82,
                h=213.64,
                l=206.39,
                n=100,
                o=206.9,
                t=1723060800000,
                v=60109650,
                vw=210.7375,
            )
        ],
        resultsCount=1,
        status="OK",
        ticker="AAPL",
        next_url=None,
    )
    mock_get_data.return_value = mock_response

    mock_constructor.return_value.construct_aggregate_bars_endpoint = MagicMock(
        return_value="mock_endpoint"
    )
    mock_service.return_value.fetch_data_with_endpoint.return_value = mock_response

    result = fetch_polygon_agg_bars()
    assert result == mock_response
