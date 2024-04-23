from typing import Any, Callable
import threading
from datetime import datetime

from attrs import define, field
import pika

from glassdolls import logger


from glassdolls.constants import EXCHANGE_NAME, RABBITMQ_CONN_PARAMS

THREADS = 1


@define
class ThreadedConsumer(threading.Thread):
    connection: "pika.BlockingConnection" = field(
        default=pika.BlockingConnection(RABBITMQ_CONN_PARAMS), repr=False
    )
    channel: "pika.adapters.blocking_connection.BlockingChannel" = field(
        init=False, repr=False
    )
    queue: str = field(default="game.queue")
    thread_name: str = field(default="")

    def __hash__(self) -> int:
        return hash((datetime.now(),))

    def __attrs_post_init__(self) -> None:
        threading.Thread.__init__(self)

        self.channel = self.connection.channel()

    def bind_queue(self, routing_key: str) -> None:
        self.channel.queue_declare(queue=self.queue, auto_delete=False)
        self.channel.queue_bind(
            queue=self.queue, exchange=EXCHANGE_NAME, routing_key=routing_key
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
