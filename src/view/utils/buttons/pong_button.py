from src.controllers.games.pong_game import PongGame
from src.view.utils.buttons.button import Button


class PongButton(Button):

    def __init__(self, manager, pathImage, x, y):
        super().__init__(manager, pathImage, x, y)

    def pressed(self):
        pong = PongGame(self.manager)
        pong.execute()
