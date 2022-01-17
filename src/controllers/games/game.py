from abc import abstractmethod


class Game:

    @abstractmethod
    def __init__(self,manager):
        self.manager=manager

    @abstractmethod
    def execute(self):
        pass
