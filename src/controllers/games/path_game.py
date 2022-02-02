import pygame
from src.controllers.games.game import Game
from src.model.components.handle import Handle
from src.model.components.path import Path

class PathGame(Game):

    def __init__(self, screen):
        super().__init__(screen,1)
        self.font=pygame.font.SysFont(None, 24)

    def execute(self):
        running = True
        score = 0
        initTimeTarget = pygame.time.get_ticks()
        path = Path()
        handlesSucceeded = []

        radius = 25

        self.setupParcours(path)

        handles = path.getHandles().copy()

        while running:
            pygame.display.flip()
            self.manager.screen.fill((0, 0, 0, 0))

            for i in range(0,len(path.getHandles())):
                pygame.draw.circle(self.manager.screen, (255, 0, 0), (path.getHandles()[i].x, path.getHandles()[i].y), path.getHandles()[i].radius)
                text = self.font.render(str(i+1), True, (255,255,255))
                self.manager.screen.blit(text, text.get_rect(center = (path.getHandles()[i].x, path.getHandles()[i].y)))

            playerPosition = self.getPlayerPosition()

            for position in playerPosition:
                if position.colliderect(pygame.Rect(handles[0].x-radius,handles[0].y-radius,radius*2,radius*2)):
                    handlesSucceeded.append(handles[0])
                    handles.remove(handles[0])
                    score += 1
                    print(score)
                    break

            for h in handlesSucceeded:
                pygame.draw.circle(self.manager.screen,(0,255,0),(h.x,h.y),radius)

            if len(handles)==0:
                self.closeCam()
                running=False

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                    self.closeCam()
                    self.manager.running = False

    def setupParcours(self,path):
        setup = True
        handles = []
        while setup:
            pygame.display.flip()
            self.manager.screen.fill((0, 0, 0, 0))
            for i in range(0, len(handles)):
                pygame.draw.circle(self.manager.screen, (255, 0, 0), (handles[i].x, handles[i].y), handles[i].radius)
                text = self.font.render(str(i + 1), True, (255, 255, 255))
                self.manager.screen.blit(text, text.get_rect(center=(handles[i].x, handles[i].y)))
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    handles.append(Handle(x, y))
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        path.setHandles(handles)
                        setup = False
                if e.type == pygame.QUIT:
                    setup = False
                    self.manager.running = False