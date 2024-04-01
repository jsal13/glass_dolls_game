import pytest
from unittest.mock import MagicMock, patch
from blessed.keyboard import Keystroke

from glassdolls.game.signals import SignalSender


def test_signal_sender_initializes() -> None:
    signal_sender = SignalSender()


@patch("glassdolls.io.signals.logger")
def test_signal_log_handle_signal_runs(mock_logger: MagicMock) -> None:
    signal_sender = SignalSender()
    signal_sender._log_handle_signal("test", data=None)
    signal_sender._log_handle_signal("test", data={"hello": 1})
