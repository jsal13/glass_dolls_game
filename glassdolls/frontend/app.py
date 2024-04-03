import streamlit as st

st.title("Glass Dolls")

code_submit_container = st.container(border=False)
code_submit_container.empty()
output_container = st.container(border=False)
output_container.empty()
solution_container = st.container(border=False)
solution_container.empty()
solution_check_container = st.container(border=False)
solution_check_container.empty()


def code_to_output(code: str) -> None:
    # No real reason to return int, just don't know what else to do here yet.
    if code is None or not code:
        txt = "Invalid or missing code."
        output_container.error(txt)
    else:
        display_problem(
            title="Mr. Toad's Wild Ride",
            problem="Here's one possible output.  Wild, right?",
        )


def get_problem(code: str) -> tuple[str, str]:
    # (title, problem)
    return ("", "")


def get_solution(code: str) -> str:
    # (title, problem)
    return "TEST"


def display_problem(title: str, problem: str) -> None:
    output_container.markdown("---")
    output_container.subheader(title)
    output_container.markdown(f":violet[{problem}]")
    output_container.markdown("---")

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
    if get_solution(code) == user_solution:
        solution_check_container.text("You did it!")
    else:
        solution_check_container.text("You did not do it!")


code = code_submit_container.text_input(label="Input Code Here", max_chars=128)
submit = code_submit_container.button("Submit", on_click=code_to_output, args=(code,))
