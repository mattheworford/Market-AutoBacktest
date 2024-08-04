# utils/alpha_vantage_api_constructor.py
class AlphaVantageApiConstructor:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def construct_time_series_daily_endpoint(self, symbol: str, api_key: str) -> str:
        return f"?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
