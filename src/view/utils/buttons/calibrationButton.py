from src.view.utils.buttons.button import Button


class calibrationButton(Button):

    def __init__(self, screen, pathImage, x, y):
        super().__init__(screen, pathImage, x, y)

    def pressed(self):
        print("BOUTON CALIBRATION PRESSED")