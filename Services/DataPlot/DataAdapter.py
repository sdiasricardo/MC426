#classe de decisao
import os, sys, shutil

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
absolute_directory = os.path.dirname(parent_directory)
sys.path.append(absolute_directory + "/ExternalConnections/api")


from FileHandler import FileHandler
from apiHandler import ApiHandler #import ok

class DataAdapter:
    def __init__(self) -> None:
        self.apihandler = ApiHandler()
        self.filehandler = FileHandler()
    
    def _search_cache(self, target_file_name):
        target = f"{target_file_name}.json"
        for root, dirs, files in os.walk(current_directory + '/DataCache/'):
            for file_name in files:
                if file_name == target:
                    return os.path.join(root, file_name)
        return None
    
    def get_data(self, query: str):
        '''
        Query: str = {City}
        '''
        cache = self._search_cache(query)
        if cache is None:
            data = self.apihandler.getJSON(query)
        else:
            data = self.filehandler.getJSON(cache)
        return data