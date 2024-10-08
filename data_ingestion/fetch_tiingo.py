import requests
import pandas as pd
from io import StringIO
import os
from dotenv import load_dotenv

from config.config import COLUMN_MAPPINGS, MARKET_DATA_COLUMNS

load_dotenv()


def fetch_tiingo_data(
    symbol: str, start_date: str = "2020-01-01", end_date: str = "2024-01-01"
) -> pd.DataFrame:
    TIINGO_API_KEY = os.getenv("TIINGO_API_KEY")
    url = f"https://api.tiingo.com/tiingo/daily/{symbol}/prices"
    params = {
        "startDate": start_date,
        "endDate": end_date,
        "token": TIINGO_API_KEY,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    csv_data = StringIO(response.text)
    data = pd.read_json(csv_data)
    return standardize_data(data)


def standardize_data(df: pd.DataFrame) -> pd.DataFrame:
    df.rename(columns=COLUMN_MAPPINGS["tiingo"], inplace=True)
    df.set_index("date", inplace=True)
    df.index = pd.to_datetime(df.index)

    return df[MARKET_DATA_COLUMNS]
