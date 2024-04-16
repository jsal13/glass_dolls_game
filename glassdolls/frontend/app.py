import os
from typing import Any
import streamlit as st
import requests

IN_DOCKER = bool(os.getenv("IN_DOCKER"))  # True if inside docker.

API_HOST_NAME = "backend" if IN_DOCKER else "localhost"
API_BASE = f"http://{API_HOST_NAME}:8001"


st.title("Glass Dolls")

code_submit_container = st.container(border=False)
code_submit_container.empty()
output_container = st.container(border=False)
output_container.empty()
solution_container = st.container(border=False)
solution_container.empty()
solution_check_container = st.container(border=False)
solution_check_container.empty()

if "output_title" not in st.session_state:
    st.session_state["output_title"] = ""
if "output_text" not in st.session_state:
    st.session_state["output_text"] = ""
if "faction_data" not in st.session_state:
    st.session_state["faction_data"] = {}


def get_random_faction_data() -> dict[Any, Any]:
    resp = requests.get(f"{API_BASE}/factions/random")
    return resp.json()


def code_to_output(code: str) -> None:
    if code is None or not code:
        txt = "Invalid or missing code."
        output_container.error(txt)
    else:
        st.session_state["faction_data"] = get_random_faction_data()
        print(st.session_state["faction_data"])
        display_problem(
            title=st.session_state["faction_data"]["name"],
            problem=st.session_state["faction_data"]["sub_cipher_translated_phrases"][
                0
            ],
        )


code = code_submit_container.text_input(label="Input Code Here", max_chars=128)
submit = code_submit_container.button("Submit", on_click=code_to_output, args=(code,))


def display_problem(title: str, problem: str) -> None:
    output_container.markdown("---")
    st.session_state["output_title"] = title
    output_container.subheader(st.session_state["output_title"])
    st.session_state["output_text"] = f":violet[{problem}]"
    output_container.markdown(st.session_state["output_text"])
    output_container.markdown("---")


def display_input_solution() -> None:
    solution = solution_container.text_input(label="Input Solution Here", max_chars=128)
    submit = solution_container.button(
        "Submit Solution",
        on_click=check_solution,
        args=(
            code,
            solution,
        ),
    )


def check_solution(code: str, user_solution: str) -> None:
    if "TEST" == user_solution:
        solution_check_container.text("You did it!")
    else:
        solution_check_container.text("You did NOT do it!")


# Session State for Rerunning page.
if st.session_state["output_title"]:
    display_problem(
        title=st.session_state["output_title"], problem=st.session_state["output_text"]
    )
    display_input_solution()

if st.session_state["faction_data"]:
    st.markdown(st.session_state["faction_data"]["phrases"][0])
