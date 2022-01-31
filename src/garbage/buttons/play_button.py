from src.garbage.buttons.button import Button


class PlayButton(Button):

    def __init__(self, manager, pathImage, x, y):
        super().__init__(manager, pathImage, x, y)

    def pressed(self):
        if self.manager.wallCalibration:
            self.manager.startMenuGame()
