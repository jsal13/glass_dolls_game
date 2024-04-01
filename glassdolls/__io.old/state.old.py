# from blessed import Terminal

# from glassdolls.game.game_text import GameText
# from glassdolls.game.screens import ScreenRenderer, ScreenTypes
# from glassdolls.game.utils import Loc

# TERM = Terminal()
# TEXT = GameText()
# SCREEN = ScreenRenderer(term=TERM)


# class UserState:

#     def __init__(
#         self,
#         current_state: ScreenTypes = ScreenTypes.STORY,
#         dungeon: str | None = None,
#         dungeon_level: str | None = None,
#         loc: Loc = Loc(x=0, y=0),
#     ) -> None:
#         self.current_state = current_state
#         self.dungeon = dungeon
#         self.dungeon_level = dungeon_level
#         self.loc = loc

#     def is_able_to_move(self) -> bool:
#         return self.current_state in [ScreenTypes.MAP]

#     def is_able_to_press_keys(self) -> bool:
#         return self.current_state in [
#             ScreenTypes.MAP,
#             ScreenTypes.STORY,
#             ScreenTypes.INPUT,
#         ]


# USER_STATE = UserState()
