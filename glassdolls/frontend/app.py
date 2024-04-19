import os
from typing import Any
import requests
from flask import Flask, render_template, request

IN_DOCKER = bool(os.getenv("IN_DOCKER"))  # True if inside docker.

API_HOST_NAME = "backend" if IN_DOCKER else "localhost"
API_BASE = f"http://{API_HOST_NAME}:8001"

app = Flask(__name__)


def get_puzzle(code: str) -> dict[str, str]:
    # TODO: Error handling, make this its own fn.
    resp = requests.get(f"{API_BASE}/code/{code}").json()
    return {"faction": resp["name"], "phrase": resp["phrases"]["sub_cipher"]}


def check_solution(code: str, user_solution: str) -> None:
    return requests.get(f"{API_BASE}/check/{code}/{user_solution}").json()["data"]


@app.route("/")
def index() -> str:
    return render_template("home.html.j2")


@app.route("/puzzle")
def puzzle() -> str:
    code = request.args.get("code", "")
    puzzle = get_puzzle(code=code)
    return render_template(
        "puzzle.html.j2", faction=puzzle["faction"], phrase=puzzle["phrase"]
    )
