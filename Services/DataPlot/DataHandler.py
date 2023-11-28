import sys, os
import json

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
absolute_directory = os.path.dirname(parent_directory)
sys.path.append(absolute_directory)
sys.path.append(absolute_directory + "/ExternalConnections/api")

from ExternalConnections.api.apiHandler import ApiHandler

#TODO ver quao diferente é current de forecast

class DataHandler:
    def __init__(self, apiHandler): #ApiHandler da aplicação inteira
        self.apiHandler = apiHandler
        self.data = None
    
    def _call_api(self, query_type: str | None = None, query_place: str | None = None):
        if query_place is None or query_type is None:
            raise Exception('query_type or query_place is None')
        self.data = self.apiHandler.queryCityWeather(query_type, query_place)

    def get_current_climate(self, query_place: str | None = None):
        self._call_api('current', query_place)
        return self.data

    #retorna uma lista de alertas
    def get_alerts(self, query_place: str | None = None):
        if query_place is None:
            raise Exception('no input for query_place')
        data = self.apiHandler.queryCityWeather('forecast', query_place)
        return data['alerts']['alert']

if __name__ == '__main__':
    api = ApiHandler()
    dh = DataHandler(api)
    dh._set_data('forecast', 'Manaus')
    with open('dataManaus.json', 'w') as f:
        json.dump(dh.data, f)




