import src
from src.controllers.switch_frame_controller import SwitchFrameController
from src.view.frames.abstract_frame import AbstractFrame
from src.view.frames.targets_frame import TargetsFrame
from src.view.items.button import Button
from src.view.listeners.action_listener import ActionListener
from src.view.frames.pong_frame import PongFrame

class GamesFrame(AbstractFrame, ActionListener):
    def __init__(self):
        AbstractFrame.__init__(self, bgImage="view/images/background.png")
        self.pongButton = Button(300, 100, text="PONG")
        self.add(self.pongButton)
        self.targetButton = Button(300, 400, text="CIBLES")
        self.add(self.targetButton)
        self.pathButton = Button(300, 700, text="PARCOURS")
        self.add(self.pathButton)
        self.returnButton = Button(1551, 919, text="RETOUR")
        self.add(self.returnButton)
        self.handlesDetectorButton = Button(900, 550, text="DETECTION PRISES")
        self.add(self.handlesDetectorButton)

        self.pongButton.addActionListener(self)
        self.targetButton.addActionListener(self)
        self.pathButton.addActionListener(self)
        self.returnButton.addActionListener(self)
        self.handlesDetectorButton.addActionListener(self)

    def execute(self):
        pass

    #TODO: use controllers, having window imbedded
    def actionPerformed(self, source):
        if source == self.pongButton:
            SwitchFrameController().control(frame=PongFrame())
        elif source == self.targetButton:
            SwitchFrameController().control(frame=TargetsFrame())
        elif source == self.pathButton:
            SwitchFrameController().control(frame=PathFrame())
        elif source == self.returnButton:
            from src.view.frames.home_frame import HomeFrame
            SwitchFrameController().control(frame=HomeFrame())
