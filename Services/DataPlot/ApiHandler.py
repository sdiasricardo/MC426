import os, sys, json

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
absolute_directory = os.path.dirname(parent_directory)
sys.path.append(absolute_directory)
sys.path.append(absolute_directory + "/Services/Dataplot/")

from DataHandler import DataHandler

class ApiHandler(DataHandler):
    def __init__(self, api_caller):
        self.ApiCaller = api_caller

    def write_cache(self, query_string, data):
        print(current_directory + '/ApiCache/' + query_string + '.json')
        with open(absolute_directory + '/Services/DataPlot/DataCache/' + query_string + '.json', 'w') as f:
            json.dump(data, f)

    def getJSON(self, query_place):
        response = self.ApiCaller.callApi(query_place)
        self.write_cache(query_place, response)
        return response
