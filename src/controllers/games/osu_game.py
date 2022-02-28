import random
import pygame

from src.controllers.games.game_singleplayer import GameSinglePlayer
from src.controllers.games.utils.target import Target


class OsuGame(GameSinglePlayer):

    def __init__(self, parent):
        super().__init__(parent)
        self.score = 0
        self.initTimeTarget = pygame.time.get_ticks()
        self.waitTimeTarget = random.randint(2000, 5000)
        self.targets = []
        self.targetsDispawned = []

    def execute(self):
        while self.continueGame:
            if (self.initTimeTarget + self.waitTimeTarget - pygame.time.get_ticks()) <= 0:
                target = Target(self.parent)
                self.targets.append(target)
                self.parent.add(target)
                self.initTimeTarget = pygame.time.get_ticks()
                self.waitTimeTarget = random.randint(2000, 4000)

            for t in self.targets:
                if t.ticks + 5000 - pygame.time.get_ticks() <= 0:
                    self.targets.remove(t)
                    self.targetsDispawned.append(t)
                    t.ticks = pygame.time.get_ticks()
                    t.failed()

            for id, limb in self.player.landmarks.items():
                radius = self.player.limbsRadius[id]
                if not limb or not radius:
                    continue

                for t in self.targets:
                    if t.collide(limb, radius):
                        self.targets.remove(t)
                        self.targetsDispawned.append(t)
                        t.ticks = pygame.time.get_ticks()
                        self.score += 1
                        print(self.score)

            for t in self.targetsDispawned:
                if t.ticks + 2000 - pygame.time.get_ticks() <=0:
                    self.targetsDispawned.remove(t)
                    self.parent.remove(t)