import json
import time
from datetime import datetime
from typing import Any, Callable

import pika
from attrs import define, field

from glassdolls import logger
from glassdolls.constants import DEFAULT_EXCHANGE, DEFAULT_QUEUE, RABBITMQ_CONN_PARAMS


@define(slots=False)
class Producer:
    exchange: str
    connection: "pika.BlockingConnection"
    channel: "pika.adapters.blocking_connection.BlockingChannel"
    queue: str

    @classmethod
    def create_standard_producer(cls) -> "Producer":
        exchange = DEFAULT_EXCHANGE
        connection = pika.BlockingConnection(RABBITMQ_CONN_PARAMS)
        channel = connection.channel()
        queue = DEFAULT_QUEUE

        _cls = cls(
            exchange=exchange, channel=channel, connection=connection, queue=queue
        )
        _cls.channel.exchange_declare(
            exchange=_cls.exchange,
            exchange_type=pika.exchange_type.ExchangeType("topic"),
        )
        return _cls

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
            json.dumps(
                {
                    "streams": [
                        {
                            "stream": {"label": "glassdolls"},
                            "values": [
                                [
                                    str(time.time_ns()),
                                    json.dumps(
                                        {
                                            "event": "send-to-queue",
                                            "routing_key": routing_key,
                                            "msg": body,
                                        }
                                    ),
                                ]
                            ],
                        }
                    ]
                }
            )
        )
