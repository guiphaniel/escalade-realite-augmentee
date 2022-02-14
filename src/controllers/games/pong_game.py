import math
import random
import pygame
from pygame.examples.playmus import Window

from src.controllers.games.game import Game
from src.controllers.games.utils.ball import Ball


class PongGame(Game):

    def __init__(self, parent):
        super().__init__(parent, 2)
        self.scorePlayer1 = 0
        self.scorePlayer2 = 0
        self.font = pygame.font.SysFont(None, 128)

        self.ball = Ball(parent)

    def execute(self):
        while self.continueGame:
            self.win.fill((0, 0, 0))

            pygame.draw.rect(self.win,(238,130,238),pygame.Rect(self.win.get_rect().centerx - 1,0,3,self.win.get_rect().height))

            playerPositionMutliple = self.getMultiplePlayerPosition()

            self.ball.collideGoal()
            self.ball.collideBorder()
            for position in playerPositionMutliple[0]:
                self.ball.collidePlayer(position)
            for position in playerPositionMutliple[1]:
                self.ball.collidePlayer(position)
            self.ball.update()
            self.ball.draw()

            if self.ball.goalRight():
                self.scorePlayer1+=1
                self.ball.spawn()
            elif self.ball.goalLeft():
                self.scorePlayer2+=1
                self.ball.spawn()

            text = self.font.render(str(self.scorePlayer1), True, (255, 255, 255))
            self.win.blit(text, text.get_rect(center=(self.win.get_rect().width/4, 50)))

            text = self.font.render(str(self.scorePlayer2), True, (255, 255, 255))
            self.win.blit(text, text.get_rect(center=((self.win.get_rect().width / 4)*3, 50)))

            pygame.display.flip()
