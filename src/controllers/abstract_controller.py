from abc import abstractmethod


class AbstractController:
    @abstractmethod
    def execute(self, **kwargs):
        pass