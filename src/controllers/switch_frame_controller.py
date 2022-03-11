import src
from src.controllers.abstract_controller import AbstractController


class SwitchFrameController(AbstractController):
    def execute(self, **kwargs):
        from src.view.window import Window
        Frame = kwargs.get("frame")
        frameArgs = kwargs.get("frameArgs")

        # remove all listeners that were previously handled by the manager, so they won't get triggered anymore
        src.view.window.Window().eventManager.removeAllListeners()

        if frameArgs:
            Window().currentFrame = Frame(**frameArgs)
        else:
            Window().currentFrame = Frame()

        Window().update()
