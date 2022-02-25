import pygame

import src
from src.controllers.games.path_game import PathGame
from src.controllers.start_game_controller import StartGameController
from src.controllers.switch_frame_controller import SwitchFrameController
from src.model.components.handle import Handle
from src.model.components.path import Path
from src.model.components.player import Player
from src.model.database import Database
from src.utils.events.keyboard_listener import KeyboardListener
from src.utils.events.motion_listener import MotionListener
from src.utils.events.mouse_listener import MouseListener
from src.view.frames.abstract_frame import AbstractFrame
from src.view.frames.path_frame import PathFrame

from src.view.internalframes.handles_in_path_editor import HandlesInPathEditor


class PathCreationFrame(AbstractFrame, MouseListener, MotionListener, KeyboardListener):

    def __init__(self, path):
        AbstractFrame.__init__(self)
        KeyboardListener.__init__(self)

        self.editorFrame = HandlesInPathEditor(path, self, (10, 10))
        self.add(self.editorFrame)

    def repaintAll(self):
        if self.bgImage:
            self.win.blit(self.bgImage, (0, 0))
        else:
            self.win.fill(self.bgColor)
        cpt = 1
        for i in self.items:
            i.draw()
            if isinstance(i, Handle):
                font = pygame.font.SysFont("view/fonts/All the Way to the Sun.otf", 40)
                textSurface = font.render(str(cpt), True, (255, 255, 255))
                self.win.blit(textSurface, i.rect.bottomright)
                cpt += 1
        pygame.display.flip()

    def onKeyboardEvent(self, e):
        if e.key == pygame.K_ESCAPE or e.type == pygame.QUIT:
            SwitchFrameController().execute(frame=src.view.frames.games_frame.GamesFrame())
            return True

        return False
