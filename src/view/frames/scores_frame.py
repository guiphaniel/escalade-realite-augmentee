from abc import abstractmethod

import pygame

from src.controllers.switch_frame_controller import SwitchFrameController
from src.model.database import Database
from src.view.frames.abstract_frame import AbstractFrame
from src.view.items.button import Button
from src.view.items.text import Text
from src.view.listeners.action_listener import ActionListener


class ScoresFrame(AbstractFrame, ActionListener):

    def __init__(self):
        AbstractFrame.__init__(self)
        ActionListener.__init__(self)

        self.backBt = Button(self, 1551, 919, text="RETOUR")
        self.add(self.backBt)

        self.backBt.addActionListener(self)
        self.scores = Database().getScores()
        self.initScoresDisplay()

    def initScoresDisplay(self):
        padding = 40
        y = padding
        for path in self.scores.keys():
            pathText = Text(self, padding, y, path.name)
            self.add(pathText)
            y += pathText.rect.h + padding
            for score in self.scores[path]:
                x = padding * 2
                playerText = Text(self, x, y, score.player.pseudo)
                self.add(playerText)
                x += playerText.rect.w + padding

                scoreText = Text(self, x, y, str(score.score))
                self.add(scoreText)
                x += scoreText.rect.w + padding

                dateText = Text(self, x, y, score.date)
                self.add(dateText)

                y += max(playerText.rect.h, scoreText.rect.h, dateText.rect.h) + padding

    def actionPerformed(self, source):
        if source == self.backBt:
            from src.view.frames.games_frame import GamesFrame
            SwitchFrameController().execute(frame=GamesFrame())
