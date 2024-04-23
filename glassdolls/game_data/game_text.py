import json

from attrs import define, field

from glassdolls.constants import DATA_GAME_DIALOGUE


@define
class GameText:
    game_text_path: str
    text: dict[str, str | list[str]]

    @classmethod
    def create_gametext(cls, game_text_path: str = DATA_GAME_DIALOGUE) -> "GameText":
        with open(game_text_path, "r", encoding="utf-8") as f:
            text = json.load(f)
        _cls = cls(game_text_path=game_text_path, text=text)
        return _cls

    def __getitem__(self, key: str) -> str | list[str]:
        return self.text[key]
