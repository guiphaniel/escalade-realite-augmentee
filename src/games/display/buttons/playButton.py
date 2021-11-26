from src.games.display.buttons.Button import Button


class playButton(Button):

    def __init__(self, screen, pathImage, x, y):
        super().__init__(screen, pathImage, x, y)

    def pressed(self):
        print("BOUTON PLAY PRESSED")