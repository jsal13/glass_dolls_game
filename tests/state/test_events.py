import pytest

from glassdolls.state.events import Event, Events


def test_map_event_initializes() -> None:
    Event()


def test_map_events_initializes() -> None:
    Events()
