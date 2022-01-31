import pygame.display

from src.utils.detectors.handle_detector import Handle_Detector
from src.garbage.buttons.button import Button


class HandleDetectorButton(Button):

    def __init__(self, manager, pathImage, x, y):
        super().__init__(manager, pathImage, x, y)

    def pressed(self):
        img = pygame.image.load("view/images/BlackScreen.png")
        self.manager.screen.blit(img, (0, 0))
        pygame.display.flip()
        self.manager.handle_detector = Handle_Detector()
        self.manager.handle_detector.startHandleDetector(self.manager)