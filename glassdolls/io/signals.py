from typing import Any

from attrs import define
from blinker import NamedSignal

from glassdolls.io import logger


@define
class SignalSender:
    """Represents objects which can send or handle signals."""

    def send_signal(
        self, signal: NamedSignal, data: dict[str, Any] | None = None
    ) -> None:
        logger.debug(
            f'SENT ("{self.__class__.__name__}") Signal: "{signal.name}".  Data: "{data}"'
        )
        signal.send(signal.name, data=data)

    def _log_handle_signal(
        self, signal: str | None, data: dict[str, Any] | None
    ) -> None:
        if signal is not None:
            logger.debug(
                f'GOT  ("{self.__class__.__name__}") Signal: "{signal}".  Data: "{data}"'
            )
