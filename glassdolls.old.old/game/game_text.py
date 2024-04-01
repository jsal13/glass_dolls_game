# import json

# from glassdolls.constants import DATA_GAME_DIALOGUE


# class GameText:
#     def __init__(self, game_text_path: str = DATA_GAME_DIALOGUE):
#         with open(game_text_path, "r", encoding="utf-8") as f:
#             self.text = json.load(f)

#     def __getitem__(self, key: str) -> list[str]:
#         return self.text[key]
