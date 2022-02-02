from src.controllers.games.path_game import PathGame
from src.garbage.buttons.button import Button


class ParcoursButton(Button):

    def __init__(self, manager, pathImage, x, y):
        super().__init__(manager, pathImage, x, y)

    def pressed(self):
        pathgame = PathGame(self.manager)
        pathgame.execute()
