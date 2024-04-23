import os
from functools import lru_cache
from typing import Any

import requests
from flask import Flask, render_template, request
from flask_caching import Cache

IN_DOCKER = bool(os.getenv("IN_DOCKER"))  # True if inside docker.

API_HOST_NAME = "backend" if IN_DOCKER else "localhost"
API_BASE = f"http://{API_HOST_NAME}:8001"

cache_config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 3600,
}
cache = Cache(config=cache_config)
app = Flask(__name__)
cache.init_app(app)


@lru_cache()
def get_puzzle(code: str) -> dict[str, str]:
    # TODO: Error handling, make this its own fn.
    resp = requests.get(f"{API_BASE}/code/{code}").json()
    return {"faction": resp["name"], "phrase": resp["phrases"]["sub_cipher"]}


@lru_cache()
def check_solution(code: str, user_solution: str) -> None:
    return requests.get(f"{API_BASE}/check/{code}/{user_solution}").json()["data"]


@cache.cached()
@app.route("/")
def index() -> str:
    return render_template("home.html.j2")


@cache.cached()
@app.route("/puzzle")
def puzzle() -> str:
    code = request.args.get("code", "")
    puzzle = get_puzzle(code=code)
    return render_template(
        "puzzle.html.j2", faction=puzzle["faction"], phrase=puzzle["phrase"]
    )
