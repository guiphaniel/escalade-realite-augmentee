from abc import abstractmethod


class Game:

    @abstractmethod
    def __init__(self,screen):
        self.screen=screen

    @abstractmethod
    def execute(self):
        pass