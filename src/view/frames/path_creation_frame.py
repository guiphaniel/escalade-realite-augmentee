import pygame

from src.controllers.games.path_game import PathGame
from src.model.components.handle import Handle
from src.view.frames.abstract_frame import AbstractFrame


class PathCreationFrame(AbstractFrame):
    def __init__(self):
        AbstractFrame.__init__(self)

        self.handles = []

    def execute(self):
        self.win.fill((0, 0, 0))
        for i in range(0, len(handles)):
            pygame.draw.circle(self.win, (255, 0, 0), (handles[i].x, handles[i].y), handles[i].radius)
            text = self.font.render(str(i + 1), True, (255, 255, 255))
            self.win.blit(text, text.get_rect(center=(handles[i].x, handles[i].y)))
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                self.handles.append(Handle(x, y))
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    path.setHandles(handles)
                    setup = False
            if e.type == pygame.QUIT:
                setup = False
                self.manager.running = False
