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
    thread_name: str = field(default="")

    def __hash__(self) -> int:
        return hash((datetime.now(),))

    def __attrs_post_init__(self) -> None:
        threading.Thread.__init__(self)

        self.channel = self.connection.channel()

    def _start_consume(
        self,
        queue: str,
        callback: Callable[..., Any],
    ) -> None:
        self.channel.basic_consume(
            queue=queue, on_message_callback=callback, consumer_tag=self.name
        )
        self.channel.start_consuming()

    def bind_queue_run(
        self, queue: str, routing_key: str, callback: Callable[..., Any]
    ) -> None:
        self.channel.queue_declare(queue=queue, auto_delete=False)
        self.channel.queue_bind(
            queue=queue, exchange=EXCHANGE_NAME, routing_key=routing_key
        )

        # This messes stuff up, weirdly.
        # self.channel.basic_qos(prefetch_count=THREADS * 10)

        thread = threading.Thread(
            name=self.name,
            target=self._start_consume,
            kwargs={
                "queue": queue,
                "callback": callback,
            },
        )

        thread.start()
