from functools import partial

import glassdolls
from glassdolls.game.components import (
    DescriptionWidget,
    InputWidget,
    HorizontalRule,
    MapRenderWidget,
)

from glassdolls.game.map import GAME_AREAS
from glassdolls.game.state import USER_STATE, TERM, TEXT, SCREEN
from glassdolls.game.utils import Loc


desc_wgt: partial[DescriptionWidget] = partial(DescriptionWidget, term=TERM)
input_wgt: partial[InputWidget] = partial(InputWidget, term=TERM)
map_wgt: partial[MapRenderWidget] = partial(MapRenderWidget, term=TERM)
horiz_rule = HorizontalRule(term=TERM)


introduction_screen = (
    desc_wgt(title="Welcome!", summary=TEXT["introduction"]),
    horiz_rule,
    input_wgt(prompt=TEXT["continue"]),
)

sample_screen = (
    desc_wgt(title="Sample!", summary=TEXT["sample"]),
    horiz_rule,
    input_wgt(prompt=TEXT["continue"]),
)

dungeon_0_level_0_screen = (
    map_wgt(area=GAME_AREAS.dungeons["Start"], map_key="0"),
    horiz_rule,
)


def main(
    screen: "glassdolls.game.screens.ScreenRenderer" = SCREEN,
    user_state: "glassdolls.game.state.UserState" = USER_STATE,
) -> None:

    screen.render_and_wait_for_key(screens=introduction_screen)
    screen.render_and_wait_for_key(screens=sample_screen)

    user_state.loc = Loc(3, 5)
    dungeon_0_level_0_screen[0].area.place_player(level="0", loc=user_state.loc)
    screen.render_and_wait_for_key(screens=dungeon_0_level_0_screen)


if __name__ == "__main__":
    main()
