import math
import random
import pygame

from src.controllers.games.game_multiplayer import GameMultiPlayer
from src.controllers.games.utils.ball import Ball

class PongGame(GameMultiPlayer):

    def __init__(self, screen):
        super().__init__(screen)

    def execute(self):
        self.running = True
        initTimeTarget = pygame.time.get_ticks()
        scorePlayer1 = 0
        scorePlayer2 = 0
        font = pygame.font.SysFont(None, 128)

        ball = Ball(self.manager)

        while self.running:
            pygame.display.flip()
            self.manager.screen.fill((0, 0, 0, 0))
            pygame.draw.rect(self.manager.screen,(238,130,238),pygame.Rect(self.manager.screen.get_rect().centerx - 1,0,3,self.manager.screen.get_rect().height))


            ball.collideGoal()
            ball.collideBorder()
            for position in list(self.playersPosition[0].values()):
                ball.collidePlayer(position)
            for position in list(self.playersPosition[1].values()):
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
                    self.closeCam()
                    self.manager.running = False
