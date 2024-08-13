import nasdaqdatalink  # type: ignore
import os
from dotenv import load_dotenv
import pandas as pd
from config.config import COLUMN_MAPPINGS, MARKET_DATA_COLUMNS

load_dotenv()


def fetch_quandl_data(
    symbol: str, start_date: str = "2018-01-01", end_date: str = "2018-12-31"
) -> pd.DataFrame:
    nasdaqdatalink.ApiConfig.api_key = os.getenv("QUANDL_API_KEY")
    data: pd.DataFrame = nasdaqdatalink.get(
        f"WIKI/{symbol}", start_date=start_date, end_date=end_date
    )
    return standardize_data(data)


def standardize_data(df: pd.DataFrame) -> pd.DataFrame:
    df.reset_index(inplace=True)
    df.rename(columns=COLUMN_MAPPINGS["quandl"], inplace=True)
    df.set_index("date", inplace=True)
    df.index = pd.to_datetime(df.index)

    return df[MARKET_DATA_COLUMNS]
