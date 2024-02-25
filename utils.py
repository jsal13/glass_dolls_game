import blessed


def refresh(term: blessed.Terminal) -> None:
    print(f"{term.home}{term.clear}")


def wait_for_enter(term: blessed.Terminal) -> None:
    with term.cbreak():
        while True:
            val = term.inkey()
            if val.is_sequence and val.name == "KEY_ENTER":
                break
