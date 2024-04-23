import threading
import json
import time
import uuid
from datetime import datetime
from typing import Any, Callable

import pika
from attrs import define, field

from glassdolls import logger
from glassdolls.constants import DEFAULT_EXCHANGE, DEFAULT_QUEUE, RABBITMQ_CONN_PARAMS


@define
class ThreadedConsumer(threading.Thread):
    connection: "pika.BlockingConnection"
    channel: "pika.adapters.blocking_connection.BlockingChannel"
    queue: str
    thread_name: str

    def __hash__(self) -> int:
        return hash((datetime.now(),))

    @classmethod
    def create_standard_threadedconsumer(
        cls, thread_name: str = uuid.uuid1().hex
    ) -> "ThreadedConsumer":
        connection = pika.BlockingConnection(RABBITMQ_CONN_PARAMS)
        channel = connection.channel()
        queue = DEFAULT_QUEUE

        _cls = cls(
            connection=connection, channel=channel, queue=queue, thread_name=thread_name
        )

        threading.Thread.__init__(_cls)
        return _cls

    def bind_queue(self, routing_key: str) -> None:
        self.channel.queue_declare(queue=self.queue, auto_delete=False)
        self.channel.queue_bind(
            queue=self.queue, exchange=DEFAULT_EXCHANGE, routing_key=routing_key
        )

    def start_thread(self, callback: Callable[..., Any]) -> None:
        # This messes stuff up, weirdly.
        # self.channel.basic_qos(prefetch_count=THREADS * 10)

        def _start_consume(callback: Callable[..., Any]) -> None:
            self.channel.basic_consume(
                queue=self.queue, on_message_callback=callback, consumer_tag=self.name
            )
            self.channel.start_consuming()

        thread = threading.Thread(
            name=self.name,
            target=_start_consume,
            kwargs={
                "callback": callback,
            },
        )

        thread.start()


def _log_consumption(routing_key: str, body: str) -> None:
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
                                        "event": "consume-from-queue",
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
