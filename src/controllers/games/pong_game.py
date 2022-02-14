import math
import random
import threading

import pygame
from pygame.examples.playmus import Window

from src.controllers.games.game import Game
from src.controllers.games.utils.ball import Ball

from src.controllers.games.game_multiplayer import GameMultiPlayer
from src.controllers.games.utils.ball import Ball

class PongGame(GameMultiPlayer):

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

            self.ball.collideBorder()
            for position in list(self.playersPosition[0].values()):
                self.ball.collidePlayer(position)
            for position in list(self.playersPosition[1].values()):
                self.ball.collidePlayer(position)
            self.ball.update(pygame.time.get_ticks()-lastFrame)
            self.ball.draw()

            if self.ball.goalRight():
                scorePlayer1+=1
                self.ball.spawn()
            elif self.ball.goalLeft():
                scorePlayer2+=1
                self.ball.spawn()

            text = self.font.render(str(self.scorePlayer1), True, (255, 255, 255))
            self.win.blit(text, text.get_rect(center=(self.win.get_rect().width/4, 50)))

            text = self.font.render(str(self.scorePlayer2), True, (255, 255, 255))
            self.win.blit(text, text.get_rect(center=((self.win.get_rect().width / 4)*3, 50)))

            lastFrame=pygame.time.get_ticks()
