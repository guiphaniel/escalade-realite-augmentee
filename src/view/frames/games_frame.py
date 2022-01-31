import src
from src.view.frames.abstract_frame import AbstractFrame
from src.view.frames.targets_frame import TargetsFrame
from src.view.items.button import Button
from src.view.listeners.action_listener import ActionListener


class GamesFrame(AbstractFrame, ActionListener):
    def __init__(self):
        AbstractFrame.__init__(self, bgImage="view/images/background.png")
        self.targetButton = Button(300, 400, text="CIBLES")
        self.add(self.targetButton)
        self.parcoursButton = Button(300, 700, text="PARCOURS")
        self.add(self.parcoursButton)
        self.pongButton = Button(300, 100, text="PONG")
        self.add(self.pongButton)
        self.returnButton = Button(1551, 919, text="RETOUR")
        self.add(self.returnButton)
        self.handlesDetectorButton = Button(900, 550, text="DETECTION PRISES")
        self.add(self.handlesDetectorButton)


        self.targetButton.addActionListener(self)
        self.parcoursButton.addActionListener(self)
        self.pongButton.addActionListener(self)
        self.returnButton.addActionListener(self)
        self.handlesDetectorButton.addActionListener(self)

    def execute(self):
        pass

    #TODO: use controllers, having window imbedded
    def actionPerformed(self, source):
        window = src.view.window.Window()
        if source == self.targetButton:
            window.currentFrame = TargetsFrame()
