from src.controllers.games.osu_game import OsuGame
from src.controllers.games.path_game import PathGame
from src.view.utils.buttons.button import Button


class OsuButton(Button):

    def __init__(self, manager, pathImage, x, y):
        super().__init__(manager, pathImage, x, y)

    def pressed(self):
        osu = OsuGame(self.manager)
        osu.execute()
