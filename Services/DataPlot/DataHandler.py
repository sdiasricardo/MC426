import sys, os
import json, shutil

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
absolute_directory = os.path.dirname(parent_directory)
sys.path.append(absolute_directory)
sys.path.append(absolute_directory + "/ExternalConnections/api")

from ExternalConnections.api.apiHandler import ApiHandler

#TODO ver quao diferente é current de forecast

class DataHandler:
    def __init__(self, apihandler: ApiHandler): #ApiHandler da aplicação inteira
        self.apihandler = apihandler

    def clear_cache(self):
        '''
        Intended to be used when the user logs out
        '''
        for file_name in os.listdir(current_directory + '/DataCache/'):
            file_path = os.path.join(current_directory + '/DataCache/', file_name)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error: {e}")

    def _search_cache(self, target_file_name):
        for root, dirs, files in os.walk(current_directory + '/DataCache/'):
            for file_name in files:
                if file_name == target_file_name:
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as file:
                        json_data = json.load(file)
                    return json_data
        return None

    def _call_api(self, query_type: str | None = None, query_place: str | None = None):
        return self.apiHandler.queryCityWeather(query_type, query_place)

    def get_current_climate(self, query_place: str | None = None):
        '''Returns a tuple containing
        [Location]
        '''
        cache = self._search_cache(query_place + '_current.json')
        if cache is None:
            data = self._call_api('current', query_place)
        return []

    #retorna uma lista de alertas
    def get_alerts(self, query_place: str | None = None):
        if query_place is None:
            raise Exception('no input for query_place')
        data = self.apiHandler.queryCityWeather('forecast', query_place)
        return data['alerts']['alert']

if __name__ == '__main__':
    # api = ApiHandler()
    # dh = DataHandler(api)
    # dh._set_data('forecast', 'Manaus')
    # with open('dataManaus.json', 'w') as f:
    #     json.dump(dh.data, f)
    ApiHandler = ApiHandler()
    teste = DataHandler(ApiHandler)



