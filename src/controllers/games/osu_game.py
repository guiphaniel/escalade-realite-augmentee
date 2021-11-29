import random
import pygame
from src.controllers.games.game import Game
from src.controllers.games.utils.target import Target


class OsuGame(Game):

    def __init__(self, screen):
        super().__init__(screen)

    def execute(self):
        running = True
        score = 0
        initTimeTarget = pygame.time.get_ticks()
        waitTimeTarget = random.randint(2000, 5000)
        targets = []
        targetsDispawned = []
        while running:
            pygame.display.flip()
            self.screen.fill((0, 0, 0, 0))
            if (initTimeTarget + waitTimeTarget - pygame.time.get_ticks()) <= 0:
                targets.append(Target(self.screen))
                initTimeTarget = pygame.time.get_ticks()
                waitTimeTarget = random.randint(2000, 4000)

            for t in targets:
                t.draw()
                x, y = pygame.mouse.get_pos()
                if t.collide(x,y):
                    targets.remove(t)
                    targetsDispawned.append(t)
                    t.ticks=pygame.time.get_ticks()
                    score+=1
                    print(score)
                elif t.ticks + 5000 - pygame.time.get_ticks() <=0:
                    targets.remove(t)
                    targetsDispawned.append(t)
                    t.ticks=pygame.time.get_ticks()
                    t.failed()

            for t in targetsDispawned:
                t.draw()
                if t.ticks + 2000 - pygame.time.get_ticks() <=0:
                    targetsDispawned.remove(t)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                    pygame.quit()