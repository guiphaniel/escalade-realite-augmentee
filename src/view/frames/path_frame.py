import pygame

from src.model.components.handle import Handle
from src.view.frames.abstract_frame import AbstractFrame


class PathFrame(AbstractFrame):
    def __init__(self):
        AbstractFrame.__init__(self)

    def repaintAll(self):
        if self.bgImage:
            self.win.blit(self.bgImage, (0, 0))
        else:
            self.win.fill(self.bgColor)
        cpt = 1
        for i in self.items:
            i.draw()
            if isinstance(i, Handle):
                font = pygame.font.SysFont("view/fonts/All the Way to the Sun.otf", 40)
                textSurface = font.render(str(cpt), True, (255, 255, 255))
                self.win.blit(textSurface, i.rect.bottomright)
                cpt += 1
        pygame.display.flip()
