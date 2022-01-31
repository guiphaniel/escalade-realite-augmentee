from src.garbage.buttons.button import Button


class ReturnButton(Button):

    def __init__(self, manager, pathImage, x, y):
        super().__init__(manager, pathImage, x, y)

    def pressed(self):
        self.manager.gameMenu=False
