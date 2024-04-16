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
    return json.loads(dumps(cursor))[0]


@api.get("/factions/{faction_name}")
def get_faction_phrases(faction_name: str) -> Any:
    MONGO_CLIENT.connect()
    return MONGO_CLIENT.query(collection="factions", query={"name": faction_name})


@api.get("/code/{code}")
def code(code: str) -> dict[Any, Any]:
    MONGO_CLIENT.connect()
    return MONGO_CLIENT.query(collection="factions", query={"phrases.code": code})[0]


@api.get("/check/{code}/{solution}")
def check_solution(code: str, solution: str) -> dict[str, bool]:
    MONGO_CLIENT.connect()
    true_solution = MONGO_CLIENT.query(
        collection="factions", query={"phrases.code": code}
    )[0]["phrases"]["solution"]
    return {"data": true_solution == solution}
