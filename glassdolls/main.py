# from functools import partial

# import glassdolls
# from glassdolls.game.components import (
#     DescriptionWidget,
#     InputWidget,
#     HorizontalRule,
#     MapRenderWidget,
#     OptionsWidget,
# )

# from glassdolls.game.map import GAME_AREAS
# from glassdolls.game.state import USER_STATE, TERM, TEXT, SCREEN
# from glassdolls.game.utils import Loc


# desc_wgt: partial[DescriptionWidget] = partial(DescriptionWidget, term=TERM)
# input_wgt: partial[InputWidget] = partial(InputWidget, term=TERM)
# map_wgt: partial[MapRenderWidget] = partial(MapRenderWidget, term=TERM)
# options_wgt: partial[OptionsWidget] = partial(OptionsWidget, term=TERM)
# horiz_rule = HorizontalRule(term=TERM)


# introduction_screen = (
#     desc_wgt(title="Welcome!", summary=TEXT["introduction"]),
#     horiz_rule,
#     input_wgt(prompt=TEXT["continue"]),
# )

# TEXT_DUNGEON_OPTIONS = TEXT["dungeon_options"]
# dungeon_0_level_0_screen = (
#     map_wgt(area=GAME_AREAS.dungeons["Start"], map_key="0"),
#     horiz_rule,
#     desc_wgt(title=TEXT["dungeon_empty_space"][0], summary=[]),
#     options_wgt(options=TEXT["dungeon_options"]),
#     horiz_rule,
# )


# def main(
#     screen: "glassdolls.game.screens.ScreenRenderer" = SCREEN,
#     user_state: "glassdolls.game.state.UserState" = USER_STATE,
# ) -> None:

#     screen.render_and_wait_for_key(screens=introduction_screen)

#     # User popped in Dungeon.
#     user_state.loc = Loc(1, 2)
#     dungeon_0_level_0_screen[0].area.place_player(level="0", loc=user_state.loc)
#     user_key = screen.render_and_wait_for_key(screens=dungeon_0_level_0_screen)
#     print(user_key)


# if __name__ == "__main__":
#     main()
