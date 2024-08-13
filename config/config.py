# Test keys
AV_API_KEY_TEST = "Str"
POLY_API_KEY_TEST = "Str"
QUANDL_API_KEY = "Str"


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
    "adjusted_volume",
]


COLUMN_MAPPINGS = {
    "quandl": {
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
        "Ex-Dividend": "ex_dividend",
        "Split Ratio": "split_ratio",
        "Adj. Open": "adjusted_open",
        "Adj. High": "adjusted_high",
        "Adj. Low": "adjusted_low",
        "Adj. Close": "adjusted_close",
        "Adj. Volume": "adjusted_volume",
    },
    "tiingo": {
        "date": "date",
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "volume": "volume",
        "adjClose": "adjusted_close",
        "adjHigh": "adjusted_high",
        "adjLow": "adjusted_low",
        "adjOpen": "adjusted_open",
        "adjVolume": "adjusted_volume",
        "divCash": "ex_dividend",
        "splitFactor": "split_ratio",
    },
    "alpha_vantage": {
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
        "5. volume": "volume",
    },
    "polygon_news": {
        "id": "article_id",
        "publisher.name": "publisher_name",
        "publisher.homepage_url": "publisher_homepage",
        "publisher.logo_url": "publisher_logo",
        "publisher.favicon_url": "publisher_favicon",
        "title": "title",
        "author": "author",
        "published_utc": "published_date",
        "article_url": "article_url",
        "tickers": "related_tickers",
        "image_url": "image_url",
        "description": "description",
        "keywords": "keywords",
        "insights": "insights",
    },
}
