from typing import Any, Sequence

from pymongo import MongoClient
from pymongo.cursor import Cursor
import psycopg
from psycopg import sql

from glassdolls.constants import MONGO_CONNECTION_STRING, PG_CONNECTION_STRING

# TODO: localhost for outside of docker, db-mongo for inside.


class MongoDB:
    """Helper Client for MongoDB."""

    def __init__(self, db: str = "glassdolls") -> None:
        self.client = self._connect()[db]

    def _connect(self) -> MongoClient[dict[str, Any]]:
        return MongoClient(host=MONGO_CONNECTION_STRING)

    def insert_values(self, collection: str, values: list[dict[str, Any]]) -> None:
        self.client[collection].insert_many(values)

    def query(self, collection: str, query: dict[str, Any]) -> Cursor[dict[str, Any]]:
        return self.client[collection].find(query)


class PostgresDB:
    """Helper Client for Postgres."""

    def __init__(self, db: str = "glassdolls") -> None:
        self.connection = self._connect()

    def _connect(self) -> psycopg.Connection:
        return psycopg.connect(conninfo=PG_CONNECTION_STRING)

    def insert_values(
        self, table: str, cols: Sequence[str], values: Sequence[Any]
    ) -> None:
        query = sql.SQL("INSERT INTO {table} ({cols}) VALUES ({values})").format(
            table=sql.Identifier(table),
            cols=sql.SQL(", ").join(map(sql.Identifier, cols)),
            values=sql.SQL(", ").join(sql.Placeholder() * len(cols)),
        )

        with self.connection.cursor() as cur:
            cur.execute(query=query, params=values)
            self.connection.commit()

    def query(self, query: str) -> list[tuple[Any, ...]]:
        # TODO: Prob should do compose here...
        # Ref: https://www.psycopg.org/psycopg3/docs/api/sql.html#psycopg.sql.Placeholder

        with self.connection.cursor() as cur:
            return cur.execute(query=query).fetchall()


if __name__ == "__main__":
    pass
    # MONGO EXAMPLE THINGS:
    # mdb = MongoDB()
    # a = [{"butt": "poop", "pee": ["1, 2, 4"], "powder": 23}]
    # mdb.insert_values(collection="phrases", values=a)
    # query = {"butt": "poop", "powder": {"$gt": 23}}
    # print([i for i in mdb.query(collection="phrases", query=query)])

    # PG EXAMPLE THINGS:
    # table = "spells"
    # cols = ("spell", "syllables")
    # values = ["Fireball", "UM OH NO"]
    # pg = PostgresDB(db="glassdolls")
    # pg.insert_values(table=table, cols=cols, values=values)
    #
    # pg = PostgresDB(db="glassdolls")
    # spells = pg.query("SELECT * FROM spells;")
    # print(spells)
