import os
import pandas as pd
import requests
from dotenv import load_dotenv
from config.config import COLUMN_MAPPINGS


load_dotenv()


def fetch_alpha_vantage_data(
    symbol: str = "SPY", output: str = "compact"
) -> pd.DataFrame:
    # AV_API_KEY = os.getenv("AV_API_KEY")
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={os.getenv("AV_API_KEY")}&outputsize={output}"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    time_series = data.get("Time Series (Daily)", {})

    df = pd.DataFrame.from_dict(time_series, orient="index")

    return standardize_data(df)


def standardize_data(df: pd.DataFrame) -> pd.DataFrame:
    df.reset_index(inplace=True)
    df.rename(columns={"index": "date"}, inplace=True)
    df.rename(columns=COLUMN_MAPPINGS["alpha_vantage"], inplace=True)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    return df[COLUMN_MAPPINGS["alpha_vantage"].values()]


print(fetch_alpha_vantage_data())
