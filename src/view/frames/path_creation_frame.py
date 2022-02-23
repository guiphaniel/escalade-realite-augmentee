import pygame

from src.controllers.games.path_game import PathGame
from src.model.components.handle import Handle
from src.utils.events.motion_listener import MotionListener
from src.utils.events.mouse_listener import MouseListener
from src.view.frames.abstract_frame import AbstractFrame
from src.view.internalframes.handlesEditorInternalFrame import HandleEditorInternalFrame

eM = HandleEditorInternalFrame.EditorMode


class PathCreationFrame(AbstractFrame, MouseListener, MotionListener):

    def __init__(self):
        AbstractFrame.__init__(self)
        MouseListener.__init__(self)
        MotionListener.__init__(self)

        self.editorMode = eM.ADD
        self.lastMousePosX = None
        self.lastMousePosY = None
        self.editedHandle = None

        self.add(HandleEditorInternalFrame(self, (10, 10)))

    def onMouseEvent(self, e) -> bool:
        pos = pygame.mouse.get_pos()
        if e.type == pygame.MOUSEBUTTONDOWN:
            if self.editorMode == eM.ADD:
                self.add(Handle(self, pos[0] - Handle.radius / 2, pos[1] - Handle.radius / 2))
                self.repaintAll()
                return True
            elif self.editorMode == eM.REMOVE:
                handle = self.findHandle(pos)
                if handle:
                    self.remove(handle)
                    self.repaintAll()
                    return True

        if self.editorMode == eM.EDIT:
            if e.type == pygame.MOUSEBUTTONDOWN:
                self.lastMousePosX, self.lastMousePosY = pos
                self.editedHandle = self.findHandle(pos)
            if e.type == pygame.MOUSEBUTTONUP:
                self.editedHandle = None
            return True

        return False

        return True

    def onMotionEvent(self, e) -> bool:
        if self.editedHandle:
            x, y = pygame.mouse.get_pos()
            newX, newY = x - self.lastMousePosX, y - self.lastMousePosY
            self.lastMousePosX, self.lastMousePosY = x, y

            self.editedHandle.move(newX, newY)

            self.repaintAll()
            return True

        return False

    def findHandle(self, coordinates):
        for h in self.items:
            if isinstance(h, Handle) and h.rect.collidepoint(coordinates):
                return h

    def repaintAll(self):
        if self.bgImage:
            self.win.blit(self.bgImage, (0, 0))
        else:
            self.win.fill(self.bgColor)
        cpt = 0
        for i in self.items:
            i.draw()
            if isinstance(i, Handle):
                font = pygame.font.SysFont("view/fonts/All the Way to the Sun.otf", 40)
                textSurface = font.render(str(cpt), True, (255, 255, 255))
                self.win.blit(textSurface, i.rect.bottomright)
                cpt += 1
        pygame.display.flip()
