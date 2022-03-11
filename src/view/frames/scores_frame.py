from abc import abstractmethod

import pygame

from src.controllers.switch_frame_controller import SwitchFrameController
from src.model.database import Database
from src.utils.events.keyboard_listener import KeyboardListener
from src.utils.events.wheel_listener import WheelListener
from src.view.frames.abstract_frame import AbstractFrame
from src.view.items.button import Button
from src.view.items.text import Text
from src.view.listeners.action_listener import ActionListener


class ScoresFrame(AbstractFrame, ActionListener, WheelListener, KeyboardListener):

    def __init__(self):
        AbstractFrame.__init__(self)
        ActionListener.__init__(self)
        WheelListener.__init__(self)
        KeyboardListener.__init__(self)

        self.padding = 40
        self.minY = 0
        self.maxY = None
        self.currentY = 0
        self.scrollIncrement = 10

        self.backBt = Button(1551, 919, text="RETOUR")
        self.add(self.backBt)

        self.backBt.addActionListener(self)
        self.scores = Database().getScores()
        self.initScoresDisplay()

    def initScoresDisplay(self):
        padding = self.padding
        y = 0
        for path in self.scores.keys():
            pathText = Text(0, y, path.name)
            self.add(pathText)
            y += pathText.rect.h + padding
            for score in self.scores[path]:
                x = padding * 2
                playerText = Text(x, y, score.player.pseudo)
                self.add(playerText)
                x += playerText.rect.w + padding

                scoreText = Text(x, y, str(score.score))
                self.add(scoreText)
                x += scoreText.rect.w + padding

                dateText = Text(x, y, score.date)
                self.add(dateText)

                y += max(playerText.rect.h, scoreText.rect.h, dateText.rect.h) + padding

        self.maxY = y - self.win.get_rect().h + self.padding

    def actionPerformed(self, source):
        if source == self.backBt:
            self.__onBack()

    def __onBack(self):
        from src.view.frames.games_frame import GamesFrame
        SwitchFrameController().execute(frame=GamesFrame)

    def onWheelEvent(self, e) -> bool:
        if e.button == 4:
            self.scrollUp()
            return True
        else:
            self.scrollDown()
            return True

        return False

    def scrollUp(self):
        if self.currentY - self.scrollIncrement >= self.minY:
            self.currentY -= self.scrollIncrement
            for i in self.items:
                if i != self.backBt:
                    i.rect.y += self.scrollIncrement

    def scrollDown(self):
        if self.currentY + self.scrollIncrement <= self.maxY:
            self.currentY += self.scrollIncrement
            for i in self.items:
                if i != self.backBt:
                    i.rect.y -= self.scrollIncrement

    def onKeyboardEvent(self, e) -> bool:
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            self.__onBack()
            return True

        return False
