import json

from attrs import define, field

from glassdolls.constants import DATA_GAME_DIALOGUE


@define
class GameText:
    game_text_path: str = field(default=DATA_GAME_DIALOGUE)
    text: dict[str, str | list[str]] = field(repr=False, init=False)

    def __attrs_post_init__(self) -> None:
        with open(self.game_text_path, "r", encoding="utf-8") as f:
            self.text = json.load(f)

    def __getitem__(self, key: str) -> str | list[str]:
        return self.text[key]
