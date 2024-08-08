import nasdaqdatalink  # type: ignore
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()


def fetch_quandl_data(
    symbol: str, start_date: str = "2018-01-01", end_date: str = "2018-12-31"
) -> pd.DataFrame:
    nasdaqdatalink.ApiConfig.api_key = os.getenv("QUANDL_API_KEY")
    data: pd.DataFrame = nasdaqdatalink.get(
        f"WIKI/{symbol}", start_date=start_date, end_date=end_date
    )
    return data
