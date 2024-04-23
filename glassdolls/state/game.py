import curses
import json
from datetime import datetime
from typing import Any

import pika
from attrs import define, field
from cattrs.preconf.json import make_converter

from glassdolls import logger
from glassdolls.io.game_screen import GameScreen
from glassdolls.io.input import UserInput
from glassdolls.pubsub.producer import Producer
from glassdolls.pubsub.threaded_consumer import ThreadedConsumer, _log_consumption
from glassdolls.state.events import Event
from glassdolls.state.map import MapState
from glassdolls.state.player import PlayerState
from glassdolls.utils import Loc


@define
class Game:
    term: "curses._CursesWindow" = field(repr=False)
    game_screen: GameScreen
    user_input: UserInput
    player_state: PlayerState
    map_state: MapState
    consumer: ThreadedConsumer = field(
        repr=False,
        default=ThreadedConsumer.create_standard_threadedconsumer(
            thread_name="game_thread"
        ),
    )
    producer: Producer = field(repr=False, default=Producer.create_standard_producer())

    @classmethod
    def create_game(
        cls,
        term: "curses._CursesWindow",
        game_screen: GameScreen,
        user_input: UserInput,
        player_state: PlayerState,
        map_state: MapState,
    ) -> "Game":

        consumer = (
            ThreadedConsumer.create_standard_threadedconsumer(
                thread_name="game_thread"
            ),
        )

        producer = Producer.create_standard_producer()

        _cls = cls(
            term=term,
            game_screen=game_screen,
            user_input=user_input,
            player_state=player_state,
            map_state=map_state,
        )

        # Signals.

        _cls.game_screen.draw_lines()
        _cls.game_screen.term.refresh()

        # User Input.
        _cls.consumer.bind_queue(routing_key="user_input.attempt_move")
        _cls.consumer.bind_queue(routing_key="user_input.look")

        # Movement.
        _cls.consumer.bind_queue(routing_key="player.loc_changed")

        # Looking.
        _cls.consumer.bind_queue(routing_key="player.look")
        _cls.consumer.bind_queue(routing_key="player.found_event")

        return _cls

    def triage(
        self,
        ch: "pika.adapters.blocking_connection.BlockingChannel",
        method: "pika.spec.Basic.Deliver",
        properties: "pika.BasicProperties",
        body: bytes,
    ) -> None:
        if method.routing_key is not None:
            _log_consumption(routing_key=method.routing_key, body=body.decode("utf-8"))
        else:
            ValueError(
                f"No routing key.  {method}, {properties}, {body.decode('utf-8')}"
            )

        data = json.loads(body.decode("utf-8"))
        # Clean.
        if method.routing_key == "user_input.attempt_move":
            if (coords := data.get("direction")) is not None:
                self.handle_user_input_attempt_movement(coords=coords)
            else:
                raise KeyError(f"No such key 'direction' in {data}.")

        elif method.routing_key == "player.loc_changed":
            if (coords := data.get("coords")) is not None:
                self.game_screen.map_display.handle_player_loc_changed(coords=coords)
            else:
                raise KeyError(f"No such key 'coords' in {data}.")

        elif method.routing_key == "user_input.look":
            self.player_state.handle_user_input_look()

        elif method.routing_key == "player.look":
            if (coords := data.get("coords")) is not None:
                self.map_state.handle_player_look(coords=coords)
            else:
                raise KeyError(f"No such key 'coords' in {data}.")

        elif method.routing_key == "player.found_event":
            if (event_json := data.get("event")) is not None:
                event = make_converter().loads(event_json, cl=Event)
                self.handle_player_found_event(event=event)
            else:
                raise KeyError(f"No such key 'event' in {data}.")

    def handle_player_found_event(self, event: Event) -> None:
        self.game_screen.description.title = event.make_title()
        self.game_screen.description.text = event.make_body()

    def handle_user_input_attempt_movement(self, coords: tuple[int, int]) -> None:
        potential_loc = self.player_state.loc + Loc.from_tuple(coords=coords)
        if not self.map_state.is_collider(loc=potential_loc):
            self.player_state.loc = potential_loc
