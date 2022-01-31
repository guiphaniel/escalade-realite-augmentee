import math
import random
import pygame
from src.controllers.games.game import Game
from src.controllers.games.utils.ball import Ball


class PongGame(Game):

    def __init__(self, screen):
        super().__init__(screen)

    def execute(self):
        running = True
        initTimeTarget = pygame.time.get_ticks()
        scorePlayer1 = 0
        scorePlayer2 = 0
        font = pygame.font.SysFont(None, 128)

        ball = Ball(self.manager)

        while running:
            pygame.display.flip()
            self.manager.screen.fill((0, 0, 0, 0))

            pygame.draw.rect(self.manager.screen,(238,130,238),pygame.Rect(self.manager.screen.get_rect().centerx - 1,0,3,self.manager.screen.get_rect().height))

            playerPosition = self.getPlayerPosition()

            ball.collideGoal()
            ball.collideBorder()
            for position in playerPosition:
                ball.collidePlayer(position)
            ball.update()
            ball.draw()

            if ball.goalRight():
                scorePlayer1+=1
                ball.spawn()
            elif ball.goalLeft():
                scorePlayer2+=1
                ball.spawn()

            text = font.render(str(scorePlayer1), True, (255, 255, 255))
            self.manager.screen.blit(text, text.get_rect(center=(self.manager.screen.get_rect().width/4, 50)))

            text = font.render(str(scorePlayer2), True, (255, 255, 255))
            self.manager.screen.blit(text, text.get_rect(center=((self.manager.screen.get_rect().width / 4)*3, 50)))

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                    self.closeCam()
                    pygame.quit()
