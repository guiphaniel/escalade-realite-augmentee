import math
import random
import threading

import pygame
from pygame.examples.playmus import Window

from src.controllers.games.game import Game
from src.controllers.games.utils.ball import Ball

from src.controllers.games.game_multiplayer import GameMultiPlayer
from src.controllers.games.utils.ball import Ball
from src.view.items.rectangle import Rectangle


class PongGame(GameMultiPlayer):

    def __init__(self, parent):
        super().__init__(parent)
        self.scorePlayer1 = 0
        self.scorePlayer2 = 0
        self.font = pygame.font.SysFont(None, 128)

        self.ball = Ball(parent)
        parent.add(self.ball)
        self.net = Rectangle(parent, self.win.get_rect().centerx - 1, 0, 3, self.win.get_rect().height)
        parent.add(self.net)

    def execute(self):
        lastFrame = pygame.time.get_ticks()

        while self.continueGame:
            self.ball.collideBorder()
            for limb in self.player1.limbs.values():
                if not limb:
                    continue
                self.ball.collidePlayer(limb)

            for limb in self.player2.limbs.values():
                if not limb:
                    continue
                self.ball.collidePlayer(limb)

            self.ball.update(pygame.time.get_ticks() - lastFrame)

            if self.ball.goalRight():
                self.scorePlayer1 += 1
                self.ball.spawn()
            elif self.ball.goalLeft():
                self.scorePlayer2 += 1
                self.ball.spawn()

            # TODO: create Item class text to display scores inside parent frame 
            # text = self.font.render(str(self.scorePlayer1), True, (255, 255, 255))
            # self.win.blit(text, text.get_rect(center=(self.win.get_rect().width / 4, 50)))
            #
            # text = self.font.render(str(self.scorePlayer2), True, (255, 255, 255))
            # self.win.blit(text, text.get_rect(center=((self.win.get_rect().width / 4) * 3, 50)))

            lastFrame = pygame.time.get_ticks()

            self.parent.repaintAll()
