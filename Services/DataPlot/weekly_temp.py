import os, sys

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
absolute_directory = os.path.dirname(parent_directory)
sys.path.append(absolute_directory + 'Services/DataPlot')

import DataInterface

class WeeklyTemp(DataInterface):
    
    def readJSON(self):
        pass

    
if __name__ == '__main__':
    teste = WeeklyTemp()
    teste.readJSON()