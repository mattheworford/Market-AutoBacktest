import os
from dotenv import load_dotenv


load_dotenv()

# Alpha Vantage
AV_API_KEY = os.getenv("AV_API_KEY")
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
QUANDL_API_KEY = os.getenv("QUANDL_API_KEY")



MARKET_DATA_COLUMNS = [
    "open",
    "high",
    "low",
    "close",
    "volume",
    "ex_dividend",
    "split_ratio",
    "adjusted_open",
    "adjusted_high",
    "adjusted_low",
    "adjusted_close",
    "adjusted_volume"
]

COLUMN_MAPPINGS = {
    "quandl": {
        'Date': 'date',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume',
        'Ex-Dividend': 'ex_dividend',
        'Split Ratio': 'split_ratio',
        'Adj. Open': 'adjusted_open',
        'Adj. High': 'adjusted_high',
        'Adj. Low': 'adjusted_low',
        'Adj. Close': 'adjusted_close',
        'Adj. Volume': 'adjusted_volume'
    },
    "tiingo": {
        'date': 'date',
        'open': 'open',
        'high': 'high',
        'low': 'low',
        'close': 'close',
        'volume': 'volume',
        'adjClose': 'adjusted_close',
        'adjHigh': 'adjusted_high',
        'adjLow': 'adjusted_low',
        'adjOpen': 'adjusted_open',
        'adjVolume': 'adjusted_volume',
        'divCash': 'ex_dividend',
        'splitFactor': 'split_ratio'
    }
}
