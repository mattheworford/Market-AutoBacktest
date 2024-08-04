import requests
import pandas as pd
from io import StringIO
import os
from dotenv import load_dotenv


def fetch_quandl_data(
    symbol: str, start_date: str = "2020-01-01", end_date: str = "2024-01-01"
) -> pd.DataFrame:
    load_dotenv()
    QUANDL_API_KEY = os.getenv("QUANDL_API_KEY")
    url = f"https://www.quandl.com/api/v3/datasets/WIKI/{symbol}.csv"
    params = {"start_date": start_date, "end_date": end_date, "api_key": QUANDL_API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()

    csv_data = StringIO(response.text)
    data = pd.read_csv(csv_data)
    return data
