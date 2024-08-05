import re


class AlphaVantageApiConstructor:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def construct_time_series_daily_endpoint(self, symbol: str, api_key: str) -> str:
        return f"?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"


class PolygonApiConstructor:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def construct_previous_close_endpoint(self, symbol: str, api_key: str) -> str:
        return f"ticker/{symbol}/prev?adjusted=true&apiKey={api_key}"

    def construct_aggregate_bars_endpoint(
        self,
        api_key: str,
        symbol: str,
        multiplier: int,
        timespan: str,
        from_: str,
        to: str,
    ) -> str:
        return f"ticker/{symbol}/range/{multiplier}/{timespan}/{from_}/{to}?adjusted=true&sort=asc&apiKey={api_key}"

    @staticmethod
    def validate_date_format(date_str: str) -> bool:
        pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        return bool(pattern.match(date_str))
