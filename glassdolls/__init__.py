import logging
from typing import Any
from logging.handlers import HTTPHandler
import requests

logger = logging.getLogger("glassdoll")
logging.basicConfig(
    filename="game_log.log", filemode="w+", encoding="utf-8", level=logging.DEBUG
)


class LokiHandler(logging.Handler):
    host = ("http://localhost:3100/loki/api/v1/push",)

    def emit(self, record: Any) -> None:
        log_entry = self.format(record)
        url = "http://localhost:3100/loki/api/v1/push"
        resp = requests.post(
            url, log_entry, headers={"Content-type": "application/json"}
        )


loki_handler = LokiHandler()
logger.addHandler(loki_handler)

# Quiet Pika, please.
logging.getLogger("pika").setLevel(logging.WARNING)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
