import pygame
from src.controllers.games.game import Game
from src.controllers.switch_frame_controller import SwitchFrameController
from src.model.components.handle import Handle
from src.model.components.path import Path
from src.model.database import Database
from src.utils.events.event_manager import EventManager
from src.utils.events.mouse_listener import MouseListener

#TODO: corriger le bug pour la création d'un parcours sans mur dans la BD -> faire une fenetre pour la creation, puis une fenetre pour le jeu
class PathGame(Game, MouseListener):

    def __init__(self, parent):
        super().__init__(parent, 1)
        EventManager().addMouseListener(self)
        self.font=pygame.font.SysFont(None, 24)
        self.score = 0
        self.path = Path()
        Database().setPathsInWall([self.path], None)
        self.handlesSucceeded = []

        self.radius = 25

        self.handles = []
        self.setup = True

    def execute(self):
        if self.setup:
            self.win.fill((0, 0, 0))
            for i in range(0, len(self.handles)):
                pygame.draw.circle(self.win, (255, 0, 0), (self.handles[i].x, self.handles[i].y), self.handles[i].radius)
                text = self.font.render(str(i + 1), True, (255, 255, 255))
                self.win.blit(text, text.get_rect(center=(self.handles[i].x, self.handles[i].y)))
            pygame.display.flip()
        else:
            self.win.fill((0, 0, 0))

            for i in range(0, len(self.path.getHandles())):
                pygame.draw.circle(self.win, (255, 0, 0), (self.path.getHandles()[i].x, self.path.getHandles()[i].y),
                                   self.path.getHandles()[i].radius)
                text = self.font.render(str(i + 1), True, (255, 255, 255))
                self.win.blit(text, text.get_rect(center=(self.path.getHandles()[i].x, self.path.getHandles()[i].y)))

            playerPosition = self.getPlayerPosition()

            for position in playerPosition:
                if position.colliderect(
                        pygame.Rect(self.handles[0].x - self.radius, self.handles[0].y - self.radius, self.radius * 2,
                                    self.radius * 2)):
                    self.handlesSucceeded.append(self.handles[0])
                    self.handles.remove(self.handles[0])
                    self.score += 1
                    print(self.score)
                    break

            for h in self.handlesSucceeded:
                pygame.draw.circle(self.win, (0, 255, 0), (h.x, h.y), self.radius)

            if len(self.handles) == 0:
                self.continueGame=False
                from src.view.frames.games_frame import GamesFrame
                SwitchFrameController().execute(frame=GamesFrame())

            pygame.display.flip()

    def onMouseEvent(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            self.handles.append(Handle(x, y))
            return True

        return False

    def onKeyboardEvent(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                self.path.setHandles(self.handles)
                self.setup = False
            if e.key == pygame.K_ESCAPE or e.type == pygame.QUIT:
                self.continueGame=False
                from src.view.frames.games_frame import GamesFrame
                SwitchFrameController().execute(frame=GamesFrame())
            return True

        return False