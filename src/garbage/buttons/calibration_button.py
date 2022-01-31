import pygame.display

from src.utils.transform import Transform
from src.garbage.buttons.button import Button


class CalibrationButton(Button):

    def __init__(self, manager, pathImage, x, y):
        super().__init__(manager, pathImage, x, y)

    def pressed(self):
        img = pygame.image.load("view/images/charucoboard.jpg")
        self.manager.screen.blit(img,(0,0))
        pygame.display.flip()
        self.manager.wallCalibration = Transform()
        self.manager.wallCalibration.startCalibration()
