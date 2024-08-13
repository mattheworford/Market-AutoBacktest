from typing import Generator, Dict, Any
import pytest
import os
from unittest.mock import patch, MagicMock
import pandas as pd
from data_ingestion.fetch_polygon_news import (
    fetch_polygon_ticker_news_data,
    standardize_data,
)


@pytest.fixture
def mock_polygon_response() -> Dict[str, Any]:
    return {
        "results": [
            {
                "id": "6da518d6e297c16898c499c58c59b13445cb0e813d755e8a4d97df343e252e70",
                "publisher": {
                    "name": "Zacks Investment Research",
                    "homepage_url": "https://www.zacks.com/",
                    "logo_url": "https://s3.polygon.io/public/assets/news/logos/zacks.png",
                    "favicon_url": "https://s3.polygon.io/public/assets/news/favicons/zacks.ico",
                },
                "title": "Market Bottom or More Downside & Volatility Ahead?",
                "author": "N/A",
                "published_utc": "2024-08-07T17:53:00Z",
                "article_url": "https://www.zacks.com/commentary/2318329/market-bottom-or-more-downside-volatility-ahead",
                "tickers": ["SPY", "QQQ"],
                "image_url": "https://staticx-tuner.zacks.com/images/articles/market-bottom.jpg",
                "description": "U.S. stocks have experienced a correction, with...",
                "keywords": ["S&P 500", "VIX", "Nasdaq 100", "Zacks Rank"],
                "insights": [
                    {
                        "ticker": "SPY",
                        "sentiment": "negative",
                        "sentiment_reasoning": "The S&P 500 Index ETF (SPY) is expected to face...",
                    },
                ],
            },
        ],
        "status": "OK",
    }


@pytest.fixture
def mock_env_vars() -> Generator[None, None, None]:
    with patch.dict(os.environ, {"POLY_API_KEY": "test_key"}):
        yield


@patch("data_ingestion.fetch_polygon_news.requests.get")
def test_fetch_polygon_ticker_news_data(
    mock_get: MagicMock, mock_polygon_response: Dict[str, Any], mock_env_vars: None
) -> None:
    mock_get.return_value.json.return_value = mock_polygon_response
    mock_get.return_value.raise_for_status = MagicMock()

    df = fetch_polygon_ticker_news_data(symbol="SPY", limit=10)

    assert not df.empty

    # Check the content of the DataFrame
    assert df.iloc[0]["publisher_name"] == "Zacks Investment Research"
    assert df.iloc[0]["title"] == "Market Bottom or More Downside & Volatility Ahead?"
    assert (
        "SPY: negative (The S&P 500 Index ETF (SPY) is expected to face...)"
        in df.iloc[0]["insights"]
    )


def test_standardize_data(mock_polygon_response: Dict[str, Any]) -> None:
    df = standardize_data(mock_polygon_response)

    assert not df.empty
    assert df.iloc[0]["publisher_name"] == "Zacks Investment Research"
    assert df.iloc[0]["title"] == "Market Bottom or More Downside & Volatility Ahead?"
    assert (
        "SPY: negative (The S&P 500 Index ETF (SPY) is expected to face...)"
        in df.iloc[0]["insights"]
    )
