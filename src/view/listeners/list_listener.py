from abc import abstractmethod


class ListListener:

    @abstractmethod
    def valueChanged(self, source):
        pass