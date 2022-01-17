import math
import random
import pygame
from src.controllers.games.game import Game
from src.controllers.games.utils.target import Target
from src.model.components.handle import Handle
from src.model.components.path import Path

class PathGame(Game):

    def __init__(self, screen):
        super().__init__(screen)
        self.font=pygame.font.SysFont(None, 24)

    def execute(self):
        running = True
        score = 0
        initTimeTarget = pygame.time.get_ticks()
        path = Path()
        handlesSucceeded = []

        radius = 25

        self.setupParcours(path,radius)

        handles = path.handles.copy()


        while running:
            pygame.display.flip()
            self.manager.screen.fill((0, 0, 0, 0))

            for i in range(0,len(path.handles)):
                pygame.draw.circle(self.manager.screen,(255,0,0),(path.handles[i].x,path.handles[i].y),radius)
                text = self.font.render(str(i+1), True, (255,255,255))
                self.manager.screen.blit(text, text.get_rect(center = (path.handles[i].x, path.handles[i].y)))



            x, y = pygame.mouse.get_pos()

            if math.sqrt((x - handles[0].x) ** 2 + (y - handles[0].y) ** 2) < radius:
                handlesSucceeded.append(handles[0])
                handles.remove(handles[0])
                score += 1
                print(score)

            for h in handlesSucceeded:
                pygame.draw.circle(self.manager.screen,(0,255,0),(h.x,h.y),radius)

            if len(handles)==0:
                running=False

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                    pygame.quit()

    def setupParcours(self,path,radius):
        setup = True
        while setup:
            pygame.display.flip()
            self.manager.screen.fill((0, 0, 0, 0))
            for i in range(0, len(path.handles)):
                pygame.draw.circle(self.manager.screen, (255, 0, 0), (path.handles[i].x, path.handles[i].y), radius)
                text = self.font.render(str(i + 1), True, (255, 255, 255))
                self.manager.screen.blit(text, text.get_rect(center=(path.handles[i].x, path.handles[i].y)))
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    path.handles.append(Handle(x, y))
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        setup = False
                if e.type == pygame.QUIT:
                    setup = False
                    pygame.quit()