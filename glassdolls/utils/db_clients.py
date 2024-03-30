from abc import ABC, abstractmethod
from typing import Any, Sequence, TypeAlias

import psycopg
from psycopg import sql
from pymongo import MongoClient
from pymongo.cursor import Cursor

from glassdolls.constants import MONGO_CONNECTION_STRING, PG_CONNECTION_STRING

# TODO: localhost for outside of docker, db-mongo for inside.


DB_Client: TypeAlias = MongoClient[dict[str, Any]] | psycopg.Connection[tuple[Any, ...]]


class DBClient(ABC):
    """Base Helper Client for DBs."""

    def __init__(self, db: str | None = "glassdolls") -> None:
        self.client: DB_Client | None = None
        self.db = db

    @abstractmethod
    def connect(self, *args: Any, **kwargs: Any) -> None: ...

    def _check_if_connected(self) -> None:
        if self.client is None:
            raise ConnectionError(
                "Client not connected.  Have you called '.connect()'?"
            )

    @abstractmethod
    def insert_values(self, *args: Any, **kwargs: Any) -> None: ...

    @abstractmethod
    def query(self, *args: Any, **kwargs: Any) -> Any: ...


class MongoDB(DBClient):
    """Helper Client for MongoDB."""

    def connect(self) -> None:
        if self.client is None:
            # PyMongo requires you to use [self.db] to define the db it's using.
            self.client: MongoClient[dict[str, Any]] = MongoClient(
                host=MONGO_CONNECTION_STRING
            )[self.db]

    def insert_values(self, collection: str, values: list[dict[str, Any]]) -> None:
        self._check_if_connected()
        self.client[collection].insert_many(values)  # type: ignore

    def query(self, collection: str, query: dict[str, Any]) -> Cursor[dict[str, Any]]:
        self._check_if_connected()
        return self.client[collection].find(query)  # type: ignore


class PostgresDB(DBClient):
    """Helper Client for Postgres."""

    def connect(self) -> None:
        self.client: psycopg.Connection[tuple[Any, ...]] = psycopg.connect(
            conninfo=PG_CONNECTION_STRING
        )

    def insert_values(
        self, table: str, cols: Sequence[str], values: Sequence[Any]
    ) -> None:
        self._check_if_connected()
        query = sql.SQL("INSERT INTO {table} ({cols}) VALUES ({values})").format(
            table=sql.Identifier(table),
            cols=sql.SQL(", ").join(map(sql.Identifier, cols)),
            values=sql.SQL(", ").join(sql.Placeholder() * len(cols)),
        )

        with self.client.cursor() as cur:
            cur.execute(query=query, params=values)
            self.client.commit()

    def query(self, query: str) -> list[tuple[Any, ...]]:
        # TODO: Prob should do compose here...
        # Ref: https://www.psycopg.org/psycopg3/docs/api/sql.html#psycopg.sql.Placeholder
        self._check_if_connected()
        with self.client.cursor() as cur:
            return cur.execute(query=query).fetchall()
