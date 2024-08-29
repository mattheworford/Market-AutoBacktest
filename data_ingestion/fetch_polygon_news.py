import os
import pandas as pd
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from config.config import COLUMN_MAPPINGS


load_dotenv()


def fetch_polygon_ticker_news_data(
    symbol: str = "AAPL", limit: int = 10
) -> Optional[pd.DataFrame]:
    print("Debug: fetch_polygon_ticker_news_data function called")
    POLY_API_KEY = os.getenv("POLY_API_KEY")
    print(f"Debug: API key is {POLY_API_KEY}")

    if not POLY_API_KEY:
        print("Error: POLY_API_KEY environment variable is not set")
        return None

    url = f"https://api.polygon.io/v2/reference/news?ticker={symbol}&limit={limit}&apiKey={POLY_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    df = standardize_data(data)
    return df


def standardize_data(data: Dict[str, Any]) -> pd.DataFrame:
    articles = data.get("results", [])
    df = pd.json_normalize(articles)
    df.rename(columns=COLUMN_MAPPINGS["polygon_news"], inplace=True)
    # flatten insights nested response field
    if "insights" in df.columns:
        df["insights"] = df["insights"].apply(
            lambda x: (
                "; ".join(
                    [
                        f"{i['ticker']}: {i['sentiment']} ({i['sentiment_reasoning']})"
                        for i in x
                    ]
                )
                if isinstance(x, list)
                else x
            )
        )
    selected_columns = list(COLUMN_MAPPINGS["polygon_news"].values())
    df = df[selected_columns]
    return df
