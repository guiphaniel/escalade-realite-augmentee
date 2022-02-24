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


class PathGame(GameSinglePlayer, MouseListener):

    def __init__(self, parent, path, player):
        GameSinglePlayer.__init__(self, parent)
        EventManager().addMouseListener(self)

        self.path = path
        self.handles = iter(path.getHandles())
        self.handlesSucceeded = []
        # self.player = player

        self.score = 0
        self.currentHandle = next(self.handles)

        for h in path.getHandles():
            parent.add(h)

        self.area = self.win.get_rect()
        self.text = Text(parent, self.area.w / 2, 20, str(self.score), (255, 255, 255))
        parent.add(self.text)

    def execute(self):
        while self.continueGame:
            for l in list(self.player.limbs.values()):
                if not l:
                    continue

                if l.colliderect(self.currentHandle.rect):
                    self.currentHandle.color = (0, 255, 0)
                    self.score += 1
                    self.text.setText(str(self.score), (255, 255, 255))

                    try:
                        self.currentHandle = next(self.handles)
                    except:  # no more handles
                        self.continueGame = False
                        SwitchFrameController().execute(frame=src.view.frames.games_frame.GamesFrame())

                    break
            if self.continueGame:
                self.parent.repaintAll()
