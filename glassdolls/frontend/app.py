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

if "output_title" not in st.session_state:
    st.session_state["output_title"] = ""
if "output_text" not in st.session_state:
    st.session_state["output_text"] = ""


def code_to_output(code: str) -> None:
    if code is None or not code:
        txt = "Invalid or missing code."
        output_container.error(txt)
    else:
        display_problem(
            title="",
            problem="",
        )


code = code_submit_container.text_input(label="Input Code Here", max_chars=128)
submit = code_submit_container.button("Submit", on_click=code_to_output, args=(code,))


def get_problem(code: str) -> tuple[str, str]:
    # (title, problem)
    return ("", "")


def get_solution(code: str) -> str:
    # (title, problem)
    return "TEST"


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
    if get_solution(code) == user_solution:
        solution_check_container.text("You did it!")
    else:
        solution_check_container.text("You did NOT do it!")


# Session State for Rerunning page.
if st.session_state["output_title"]:
    display_problem(
        title=st.session_state["output_title"], problem=st.session_state["output_text"]
    )
    display_input_solution()
