from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from typing import Any, Dict
import pandas as pd
from config.config import COLUMN_MAPPINGS
import os
from dotenv import load_dotenv

load_dotenv()


class DBService:
    def __init__(
        self,
        db_url: str = f"postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@localhost:5433/{os.getenv("DB_NAME")}",
    ):
        self.engine = create_engine(db_url)

    def upload_data(self, data: pd.DataFrame, table_name: str) -> None:
        with self.engine.connect() as conn:
            data.to_sql(table_name, conn, if_exists="append", index=False)
            print(f"Data uploaded to table {table_name}")

    def upload_polygon_news(self, data: pd.DataFrame) -> None:
        standardized_data = self._standardize_polygon_news(data)
        self.upload_data(standardized_data, "polygon_news")

    def upload_quandl_data(self, data: pd.DataFrame) -> None:
        standardized_data = self._standardize_quandl_data(data)
        self.upload_data(standardized_data, "quandl_market_data")

    def upload_tiingo_data(self, data: pd.DataFrame) -> None:
        standardized_data = self._standardize_tiingo_data(data)
        self.upload_data(standardized_data, "tiingo_market_data")

    def _standardize_polygon_news(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.rename(columns=COLUMN_MAPPINGS["polygon_news"])

    def _standardize_quandl_data(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.rename(columns=COLUMN_MAPPINGS["quandl"])

    def _standardize_tiingo_data(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.rename(columns=COLUMN_MAPPINGS["tiingo"])
