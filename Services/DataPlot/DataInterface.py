from abc import ABC, abstractmethod


class DataInterface(ABC):

    @abstractmethod
    def readJSON(self):
        pass

