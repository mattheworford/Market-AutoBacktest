import os
from dotenv import load_dotenv


load_dotenv()

# Alpha Vantage
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://www.alphavantage.co/query"
SYMBOL = "SPY"
OUTPUT = "compact"

# Polgygon
POLY_API_KEY = os.getenv("POLY_API_KEY")
POLY_BASE_URL = "https://api.polygon.io/v2/aggs/"
POLY_SYMBOL = "AAPL"
POLY_MULTIPLIER = 5
POLY_TIMESPAN = "day"
POLY_FROM_ = "2023-08-01"
POLY_TO = "2024-08-04"


# Quandl
QUANDL_API_KEY = "STR"

