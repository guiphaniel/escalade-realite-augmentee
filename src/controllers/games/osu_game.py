import random
import pygame

from src.controllers.games.game_singleplayer import GameSinglePlayer
from src.controllers.games.utils.target import Target


class OsuGame(GameSinglePlayer):

    def __init__(self, manager):
        super().__init__(manager)

    def execute(self):
        self.running = True
        score = 0
        initTimeTarget = pygame.time.get_ticks()
        waitTimeTarget = random.randint(2000, 5000)
        targets = []
        targetsDispawned = []
        while self.running:
            pygame.display.flip()
            self.manager.screen.fill((0, 0, 0, 0))
            if (initTimeTarget + waitTimeTarget - pygame.time.get_ticks()) <= 0:
                targets.append(Target(self.manager.screen))
                initTimeTarget = pygame.time.get_ticks()
                waitTimeTarget = random.randint(2000, 4000)

            for t in targets:
                t.draw()
                if t.ticks + 5000 - pygame.time.get_ticks() <= 0:
                    targets.remove(t)
                    targetsDispawned.append(t)
                    t.ticks = pygame.time.get_ticks()
                    t.failed()

            positionPlayer = self.getPlayerPosition()

            for position in positionPlayer:
                for t in targets:
                    if t.collide(position):
                        targets.remove(t)
                        targetsDispawned.append(t)
                        t.ticks = pygame.time.get_ticks()
                        score += 1
                        print(score)

            for t in targetsDispawned:
                t.draw()
                if t.ticks + 2000 - pygame.time.get_ticks() <=0:
                    targetsDispawned.remove(t)

            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.closeCam()
                        self.running = False
                if e.type == pygame.QUIT:
                    self.closeCam()
                    self.running=False
                    self.manager.running = False