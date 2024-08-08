import psycopg2
from psycopg2.extensions import connection, cursor
from typing import Any


class PostgresClient:
    def __init__(
        self, dbname: str, user: str, password: str, host: str = "localhost"
    ) -> None:
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.conn: connection = self._connect()

    def _connect(self) -> connection:
        return psycopg2.connect(
            dbname=self.dbname, user=self.user, password=self.password, host=self.host
        )

    def get_cursor(self) -> cursor:
        return self.conn.cursor()

    def execute(self, query: str, params: Any = None) -> None:
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            self.conn.commit()

    def close(self) -> None:
        self.conn.close()
