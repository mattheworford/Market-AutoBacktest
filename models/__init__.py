"""
models package

This package provides data class models for each API response. The purpose of this package is to 
cross-validate responses prior to loading them into the database. Cross-validation will highlight discrepancies,
if any, between the data providers listed below.

Providers: Quandl, Polygon.io, Tiingo, and Alpha Vantage.
"""

__version__ = "1.0.0"
__author__ = "Willem Seethaler"

import logging

# Create a logger for the package
logger = logging.getLogger(__name__)

# Configure the logger if it has no handlers
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Expose key data classes at the package level
from .alpha_vantage_daily import AlphaVantageData
from .polygon_news_data import PolygonNewsData
from .quandl_data_model import QuandlData
from .tiingo_data_model import TiingoData

logger.info("models package initialized")

__all__ = ["AlphaVantageData", "PolygonNewsData", "QuandlData", "TiingoData"]
