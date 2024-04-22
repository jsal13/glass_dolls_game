import json
from typing import Any, Callable
import time

from attrs import define, field
import pika

from glassdolls import logger

CONN_PARAMS: "pika.ConnectionParameters" = pika.ConnectionParameters("localhost")


@define(slots=False)
class RabbitMQClient:
    exchange: str = field(default="game")
    connection: "pika.BlockingConnection" = field(
        default=pika.BlockingConnection(CONN_PARAMS), repr=False
    )
    channel: "pika.adapters.blocking_connection.BlockingChannel" = field(
        init=False, repr=False
    )

    def init_rabbitmqclient(self) -> None:
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=self.exchange,
            exchange_type=pika.exchange_type.ExchangeType("topic"),
        )

    def bind_queue(self, queue: str, routing_key: str) -> None:
        # Create and bind the queue.
        self.channel.queue_declare(queue=queue)
        self.channel.queue_bind(
            exchange=self.exchange, queue=queue, routing_key=routing_key
        )

    def send_to_queue(self, routing_key: str, body: dict[str, Any]) -> None:
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key,
            body=json.dumps(body).encode("utf-8"),
        )
        logger.debug(f" [x] Sent '{body}' with routing key {routing_key}")

    def consume_from_queue(self, queue: str, callback: Callable[..., Any]) -> None:
        self.basic_get(queue=queue, auto_ack=True, on_message_callback=callback)

    def close(self) -> None:
        """Close connection."""
        self.connection.close()

    def sample_callback(
        self,
        ch: "pika.adapters.blocking_connection.BlockingChannel",
        method: "pika.spec.Basic.Deliver",
        properties: "pika.BasicProperties",
        body: bytes,
    ) -> None:
        logger.debug(
            f" [x] Received [r_key: {method.routing_key}] {json.loads(body.decode('utf-8'))}"
        )
