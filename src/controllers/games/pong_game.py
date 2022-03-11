import math
import random
import threading

import pygame
from src.controllers.games.game import Game
from src.controllers.games.utils.ball import Ball

from src.controllers.games.game_multiplayer import GameMultiPlayer
from src.controllers.games.utils.ball import Ball
from src.view.items.rectangle import Rectangle
from src.view.items.text import Text


class PongGame(GameMultiPlayer):

    def __init__(self):
        from src.view.window import Window
        super().__init__(Window().currentFrame)
        self.scorePlayer1 = 0
        self.scorePlayer2 = 0
        self.area = self.win.get_rect()

        self.ball = Ball()
        self.parent.add(self.ball)
        self.net = Rectangle(self.parent, self.area.centerx - 1, 0, 3, self.area.height)
        self.parent.add(self.net)
        self.scorePlayer1Text = Text(self.parent, self.area.w / 4, 50, str(0), (255, 255, 255), 120)
        self.parent.add(self.scorePlayer1Text)
        self.scorePlayer2Text = Text(self.parent, self.area.w / 4 * 3, 50, str(0), (255, 255, 255), 120)
        self.parent.add(self.scorePlayer2Text)

    def execute(self):
        lastFrame = pygame.time.get_ticks()

        while self.continueGame:
            self.ball.collideBorder()
            for id, l in self.player1.landmarks.items():
                radius = self.player1.limbsRadius[id]
                if not l or not radius:
                    continue
                self.ball.collidePlayer(l, radius)

            for id, l in self.player2.landmarks.items():
                radius = self.player2.limbsRadius[id]
                if not l or not radius:
                    continue
                self.ball.collidePlayer(l, radius)

            self.ball.update(pygame.time.get_ticks() - lastFrame)

            if self.ball.goalRight():
                self.scorePlayer1 += 1
                self.scorePlayer1Text.setText(str(self.scorePlayer1), (255, 255, 255), 120)
                self.ball.spawn()
            elif self.ball.goalLeft():
                self.scorePlayer2 += 1
                self.scorePlayer2Text.setText(str(self.scorePlayer2), (255, 255, 255), 120)
                self.ball.spawn()

            lastFrame = pygame.time.get_ticks()