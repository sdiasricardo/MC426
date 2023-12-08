import os, sys
import json, shutil

current_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_directory)

from DataHandler import DataHandler

class FileHandler(DataHandler):
    
    def getJSON(self, file_path: str):
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        return json_data