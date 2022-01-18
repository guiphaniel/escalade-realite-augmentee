import math
import random
import pygame
from src.controllers.games.game import Game

class PongGame(Game):

    def __init__(self, screen):
        super().__init__(screen)

    def execute(self):
        running = True
        score = 0
        initTimeTarget = pygame.time.get_ticks()

        while running:
            pygame.display.flip()
            self.manager.screen.fill((0, 0, 0, 0))

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                    self.closeCam()
                    pygame.quit()
