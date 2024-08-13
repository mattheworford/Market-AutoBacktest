import pandas as pd
import os
from pandas import DataFrame
from sqlalchemy import create_engine
from data_ingestion import fetch_quandl_data, fetch_tiingo_data


def combine_data(dataframes: list[pd.DataFrame]) -> pd.DataFrame:
    return pd.concat(dataframes, axis=0).drop_duplicates().sort_index()


def save_to_csv(data: pd.DataFrame, filepath: str) -> None:
    data.to_csv(filepath, index=True)
    print(f"Data saved to {filepath}")


def save_to_database(data: pd.DataFrame, table_name: str, db_url: str) -> None:
    engine = create_engine(db_url)
    data.to_sql(table_name, engine, if_exists="replace", index=True)
    print(f"Data saved to table {table_name} in the database.")
