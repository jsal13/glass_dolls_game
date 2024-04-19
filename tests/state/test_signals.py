import pytest
from unittest.mock import MagicMock, patch

from glassdolls.state.signals import SignalSender


def test_signal_sender_initializes() -> None:
    SignalSender()


@patch("glassdolls.io.signals.logger")
def test_signal_log_handle_signal_runs(mock_logger: MagicMock) -> None:
    signal_sender = SignalSender()
    signal_sender._log_handle_signal("test", data=None)
    signal_sender._log_handle_signal("test", data={"hello": 1})
