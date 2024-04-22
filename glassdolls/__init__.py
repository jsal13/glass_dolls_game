import logging

logger = logging.getLogger()
logging.basicConfig(
    filename="game_log.log", filemode="w+", encoding="utf-8", level=logging.DEBUG
)

logging.getLogger("pika").setLevel(logging.WARNING)
