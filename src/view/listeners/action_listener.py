from abc import abstractmethod


class ActionListener():
    @abstractmethod
    def actionPerformed(self, source):
        pass