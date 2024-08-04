import unittest
from utils.api_constructor_utils import AlphaVantageApiConstructor


class TestAlphaVantageApiConstructor(unittest.TestCase):
    def test_construct_time_series_daily_endpoint(self):
        constructor = AlphaVantageApiConstructor(
            base_url="https://www.alphavantage.co/query"
        )
        endpoint = constructor.construct_time_series_daily_endpoint(
            symbol="IBM", api_key="fake_api_key"
        )

        expected_endpoint = "?function=TIME_SERIES_DAILY&symbol=IBM&apikey=fake_api_key"
        self.assertEqual(endpoint, expected_endpoint)


if __name__ == "__main__":
    unittest.main()
