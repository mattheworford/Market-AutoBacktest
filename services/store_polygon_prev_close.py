from typing import Any, Dict
from datetime import datetime
from client.postgresql import PostgresClient


class StoreAPIService:
    def __init__(self, db_client: PostgresClient) -> None:
        self.db_client = db_client

    def create_table(self) -> None:
        current_date = datetime.now().strftime("%Y_%m_%d")
        table_name = f"{current_date}_polygon_response"
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            adjusted BOOLEAN,
            query_count INTEGER,
            request_id TEXT,
            ticker TEXT,
            c FLOAT,
            h FLOAT,
            l FLOAT,
            o FLOAT,
            t BIGINT,
            v BIGINT,
            vw FLOAT
        )
        """
        self.db_client.execute(create_table_query)

    def store_response(self, api_response: Dict[str, Any]) -> None:
        current_date = datetime.now().strftime("%Y_%m_%d")
        table_name = f"api_responses_{current_date}"
        insert_query = f"""
        INSERT INTO {table_name} (adjusted, query_count, request_id, ticker, c, h, l, o, t, v, vw)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        result = api_response["results"][0]
        params = (
            api_response.get("adjusted"),
            api_response.get("queryCount"),
            api_response.get("request_id"),
            result.get(
                "T"
            ),  # Look into why get method is not registering as a class method on result object
            result.get("c"),
            result.get("h"),
            result.get("l"),
            result.get("o"),
            result.get("t"),
            result.get("v"),
            result.get("vw"),
        )
        self.db_client.execute(insert_query, params)
