from src.controllers.games.osu_game import OsuGame
from src.controllers.games.path_game import PathGame
from src.view.utils.buttons.button import Button


class playButton(Button):

    def __init__(self, screen, pathImage, x, y):
        super().__init__(screen, pathImage, x, y)

    def pressed(self):
        pathgame = PathGame(self.screen)
        pathgame.execute()
