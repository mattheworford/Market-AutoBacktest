"""
data_ingestion package

This package provides tools for fetching and processing financial data from various sources like
Quandl, Polygon.io, Tiingo, and Alpha Vantage.
"""

__version__ = "1.0.0"
__author__ = "Matthew Orford & Willem Seethaler"

from typing import Any, Dict, List, Union, Optional
import pandas as pd
import logging

# Set up logging for the package
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Expose key functions at the package level
# from .fetch_polygon_news import fetch_polygon_ticker_news_data
# from .fetch_quandl import fetch_quandl_data
# from .fetch_tiingo import fetch_tiingo_data
# from .fetch_alpha_vantage import fetch_alpha_vantage_data


# Expose key functions at the package level
# Use lazy import pattern to avoid circular imports
def fetch_polygon_ticker_news_data(*args: Any, **kwargs: Any) -> Optional[pd.DataFrame]:
    from .fetch_polygon_news import fetch_polygon_ticker_news_data as _fetch

    return _fetch(*args, **kwargs)


def fetch_quandl_data(*args: Any, **kwargs: Any) -> pd.DataFrame:
    from .fetch_quandl import fetch_quandl_data as _fetch

    return _fetch(*args, **kwargs)


def fetch_tiingo_data(*args: Any, **kwargs: Any) -> pd.DataFrame:
    from .fetch_tiingo import fetch_tiingo_data as _fetch

    return _fetch(*args, **kwargs)


# def fetch_alpha_vantage_data(*args: Any, **kwargs: Any) -> pd.DataFrame:
#     from .fetch_alpha_vantage import fetch_alpha_vantage_data as _fetch

#     return _fetch(*args, **kwargs)


# Optional: Initialize package-wide settings or constants
DEFAULT_START_DATE = "2020-01-01"
DEFAULT_END_DATE = "2024-01-01"

logger.info("data_ingestion package initialized")

__all__ = [
    "fetch_quandl_data",
    # "fetch_alpha_vantage_data",
    "fetch_polygon_ticker_news_data",
    "fetch_tiingo_data",
]
