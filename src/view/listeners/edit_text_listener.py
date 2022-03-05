from abc import abstractmethod


class EditTextListener:

    @abstractmethod
    def onEditTextResult(self, source):
        pass