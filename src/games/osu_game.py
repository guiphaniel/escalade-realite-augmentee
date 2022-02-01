import random
import pygame
from src.games.game import Game
from src.games.utils.target import Target
from src.view.events.event_manager import EventManager
from src.view.listeners.action_listener import ActionListener


class OsuGame(Game):

    def __init__(self):
        super().__init__(1)
        self.score = 0
        self.initTimeTarget = pygame.time.get_ticks()
        self.waitTimeTarget = random.randint(2000, 5000)
        self.targets = []
        self.targetsDispawned = []

    def execute(self):
        self.win.fill((0, 0, 0))
        if (self.initTimeTarget + self.waitTimeTarget - pygame.time.get_ticks()) <= 0:
            self.targets.append(Target())
            self.initTimeTarget = pygame.time.get_ticks()
            self.waitTimeTarget = random.randint(2000, 4000)

        for t in self.targets:
            t.draw()
            if t.ticks + 5000 - pygame.time.get_ticks() <= 0:
                self.targets.remove(t)
                self.targetsDispawned.append(t)
                t.ticks = pygame.time.get_ticks()
                t.failed()

        positionPlayer = self.getPlayerPosition()

        for position in positionPlayer:
            for t in self.targets:
                if t.collide(position):
                    self.targets.remove(t)
                    self.targetsDispawned.append(t)
                    t.ticks = pygame.time.get_ticks()
                    self.score += 1
                    print(self.score)

        for t in self.targetsDispawned:
            t.draw()
            if t.ticks + 2000 - pygame.time.get_ticks() <=0:
                self.targetsDispawned.remove(t)

        pygame.display.flip()