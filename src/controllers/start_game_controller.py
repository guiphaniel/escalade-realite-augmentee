import threading
from src.controllers.abstract_controller import AbstractController


class StartGameController(AbstractController):
    def execute(self, **kwargs):
        game = kwargs.get("game")
        thread = threading.Thread(target=game.execute)
        thread.start()
