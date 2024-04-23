import json
from typing import Any, Callable
import time
from datetime import datetime

from attrs import define, field
import pika

from glassdolls import logger
from glassdolls.constants import RABBITMQ_CONN_PARAMS


@define(slots=False)
class Producer:
    exchange: str = field(default="game")
    connection: "pika.BlockingConnection" = field(
        default=pika.BlockingConnection(RABBITMQ_CONN_PARAMS), repr=False
    )
    channel: "pika.adapters.blocking_connection.BlockingChannel" = field(
        init=False, repr=False
    )
    queue: str = field(default="game.queue")

    def __attrs_post_init__(self) -> None:
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=self.exchange,
            exchange_type=pika.exchange_type.ExchangeType("topic"),
        )

    def bind_queue(self, routing_key: str) -> None:
        # Create and bind the queue.
        self.channel.queue_declare(queue=self.queue)
        self.channel.queue_bind(
            exchange=self.exchange, queue=self.queue, routing_key=routing_key
        )

    def send_to_queue(self, routing_key: str, body: dict[str, Any]) -> None:
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key,
            body=json.dumps(body).encode("utf-8"),
        )
        logger.debug(
            f" [x] {datetime.now().isoformat()} Sent `{body}` with routing key `{routing_key}`"
        )
