from src.view.utils.frames.abstract_frame import AbstractFrame
from src.view.utils.items.button import Button
from src.view.utils.listeners.action_listener import ActionListener


class HomeFrame(AbstractFrame, ActionListener):
    def __init__(self, bgColor=(50, 50, 50), bgImage = None):
        AbstractFrame.__init__(self, bgColor, bgImage)
        testButton = Button(40, 40, 40, 40, "Calibration")
        testButton.addActionListener(self)
        self.add(testButton)
        self.repaintAll()

    def execute(self):
        pass

    def actionPerformed(self, src):
        print("action")
