import os
import json
from typing import Any
from fastapi import FastAPI
from bson.json_util import dumps

from db_clients import MongoDB  # type: ignore


api = FastAPI()
MONGO_CLIENT = MongoDB()
MONGO_CLIENT.connect()


@api.get("/factions/random")
def get_faction_random() -> Any:
    MONGO_CLIENT.connect()
    cursor = MONGO_CLIENT.client["factions"].aggregate([{"$sample": {"size": 1}}])
    return json.loads(dumps(cursor))


@api.get("/factions/{faction_name}")
def get_faction(faction_name: str) -> dict[Any, Any]:
    MONGO_CLIENT.connect()
    return list(
        MONGO_CLIENT.query(collection="factions", query={"name": faction_name})
    )[0]
