import math

import pygame

import src
from src.controllers.games.game_singleplayer import GameSinglePlayer
from src.controllers.switch_frame_controller import SwitchFrameController
from src.model.components.handle import Handle
from src.model.components.path import Path
from src.model.database import Database
from src.utils.events.event_manager import EventManager
from src.utils.events.mouse_listener import MouseListener

# TODO: corriger le bug pour la création d'un parcours sans mur dans la BD -> faire une fenetre pour la creation, puis une fenetre pour le jeu
from src.view.items.text import Text


class PathGame(GameSinglePlayer):

    def __init__(self, parent, path, player):
        GameSinglePlayer.__init__(self, parent, player)

        self.path = path
        self.handles = iter(path.getHandles())
        self.handlesSucceeded = []

        self.score = pygame.time.get_ticks()
        self.currentHandle = next(self.handles)

        cpt = 1
        for h in path.getHandles():
            parent.add(h)
            parent.add(Text(parent, *h.rect.bottomright, str(cpt), (255, 255, 255)))
            cpt += 1

        self.area = self.win.get_rect()
        self.scoreText = Text(parent, self.area.w / 2, 100, str(0), (255, 255, 255), 120)
        parent.add(self.scoreText)

    def execute(self):
        while self.continueGame:
            for id, l in self.player.landmarks.items():
                radius = self.player.limbsRadius[id]
                if not l or not radius:
                    continue

                if (radius + (self.currentHandle.rect.width / 2)) > math.sqrt(
                        (l[0] - self.currentHandle.rect.centerx) ** 2 + (l[1] - self.currentHandle.rect.centery) ** 2):
                    self.currentHandle.color = (0, 255, 0)

                    try:
                        self.currentHandle = next(self.handles)
                    except:  # no more handles
                        self.continueGame = False
                        SwitchFrameController().execute(frame=src.view.frames.games_frame.GamesFrame())

                    break

            self.scoreText.setText(str((pygame.time.get_ticks() - self.score) / 1000), (255, 255, 255), 120)
