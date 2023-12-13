import sys, os, shutil
from abc import ABC, abstractmethod

class DataHandler(ABC):

    @abstractmethod
    def getJSON(self):
        pass

