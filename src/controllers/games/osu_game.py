import random
import pygame

from src.controllers.games.game_singleplayer import GameSinglePlayer
from src.controllers.games.utils.target import Target
from src.model.components.player import Player
from src.view.items.text import Text


class OsuGame(GameSinglePlayer):

    def __init__(self, parent):
        super().__init__(parent, Player(parent))
        self.area = self.win.get_rect()
        self.touched = 0
        self.missed = 0
        self.initTimeTarget = pygame.time.get_ticks()
        self.waitTimeTarget = random.randint(2000, 5000)
        self.targets = []
        self.targetsDispawned = []
        self.touchedText = Text(parent, self.area.w / 2 - 400, 100, "Touchées : 0", (255, 255, 255), 60)
        parent.add(self.touchedText)
        self.missedText = Text(parent, self.area.w / 2 + 150, 100, "Manquées : 0", (255, 255, 255), 60)
        parent.add(self.missedText)

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
                    self.missed += 1
                    self.missedText.setText("Manquées : " + str(self.missed), (255, 255, 255), 60)

            for id, limb in self.player.landmarks.items():
                radius = self.player.limbsRadius[id]
                if not limb or not radius:
                    continue

                for t in self.targets:
                    if t.collide(limb, radius):
                        self.targets.remove(t)
                        self.targetsDispawned.append(t)
                        t.ticks = pygame.time.get_ticks()
                        self.touched += 1
                        self.touchedText.setText("Touchées : " + str(self.touched), (255, 255, 255), 60)

            for t in self.targetsDispawned:
                if t.ticks + 2000 - pygame.time.get_ticks() <=0:
                    self.targetsDispawned.remove(t)
                    self.parent.remove(t)