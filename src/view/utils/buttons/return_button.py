from src.controllers.games.osu_game import OsuGame
from src.controllers.games.path_game import PathGame
from src.controllers.games.pong_game import PongGame
from src.view.utils.buttons.button import Button


class ReturnButton(Button):

    def __init__(self, manager, pathImage, x, y):
        super().__init__(manager, pathImage, x, y)

    def pressed(self):
        pong = PongGame(self.manager)
        pong.execute()
        self.manager.gameMenu=False
