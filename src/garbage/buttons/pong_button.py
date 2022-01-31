from src.games import PongGame
from src.garbage.buttons.button import Button


class PongButton(Button):

    def __init__(self, manager, pathImage, x, y):
        super().__init__(manager, pathImage, x, y)

    def pressed(self):
        pong = PongGame(self.manager)
        pong.execute()
