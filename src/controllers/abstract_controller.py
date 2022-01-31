from abc import abstractmethod


class AbstractController:
    @abstractmethod
    def control(self, **kwargs):
        pass