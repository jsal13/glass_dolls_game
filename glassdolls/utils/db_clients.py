from typing import Any
from pymongo import MongoClient

MONGO_CONNECTION_STRING = "mongodb://admin:example@db-mongo:27017/"


class MongoDB:

    def __init__(self, db: str = "glassdolls") -> None:
        self.client = self._connect()["glassdolls"]

    def _connect(self) -> MongoClient[dict[str, Any]]:
        return MongoClient(host=MONGO_CONNECTION_STRING)


if __name__ == "__main__":
    mdb = MongoDB()
    db_obj = mdb.client
    collection_phrases_obj = db_obj["phrases"]

    # collection.insert_many([{"whats": "up", "ding": "dongs"}])
