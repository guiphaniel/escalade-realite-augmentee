import random
import pygame
from src.games.game import Game
from src.games.utils.target import Target
from src.view.events.event_manager import EventManager
from src.view.listeners.action_listener import ActionListener


class OsuGame(Game):

    def __init__(self):
        super().__init__()

    def execute(self):
        running = True
        score = 0
        initTimeTarget = pygame.time.get_ticks()
        waitTimeTarget = random.randint(2000, 5000)
        targets = []
        targetsDispawned = []
        while running:
            self.win.fill((0, 0, 0, 0))
            if (initTimeTarget + waitTimeTarget - pygame.time.get_ticks()) <= 0:
                targets.append(Target())
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

            pygame.display.flip()
            #TODO: add listeners to exit game on ESC pressed (running = false, et redirection vers game menu)