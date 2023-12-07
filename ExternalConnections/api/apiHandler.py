import requests
import os, sys
#TODO: Colocar dotenv como dependencia do projeto
from dotenv import load_dotenv
import json
import pandas as pd

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
absolute_directory = os.path.dirname(parent_directory)
sys.path.append(absolute_directory)
sys.path.append(absolute_directory + "/Services/Dataplot/")

load_dotenv()
api_key = os.getenv("weather_api_key")

class ApiHandler():

    def write_cache(self, query_string, data):
        print(current_directory + '/ApiCache/' + query_string + '.json')
        with open(absolute_directory + '/Services/DataPlot/DataCache/' + query_string + '.json', 'w') as f:
            json.dump(data, f)


    def queryCityWeather(self, query_type: str, query_place: str):
        '''
        Parameters:
        query_type: current or forecast
        query_place: string representing a city or a tuple [latitude, longitude]
        Stores the api response at DataCache folder
        '''
        if isinstance(query_place, tuple):
            query_place = str(query_place[0]) + ',' + str(query_place[1])
        base_url = f'http://api.weatherapi.com/v1/{query_type}.json?key={api_key}&q={query_place}&days=7&aqi=no&alerts=yes'
        response = requests.get(base_url)
        if response.status_code == 200:
            response = response.json()
            self.write_cache(query_place + '_' + query_type, response)
            return response
        else:
            raise Exception(f'Weather API responded with code {response.status_code}')
        

if __name__ == '__main__':
    teste = ApiHandler()
    print(teste.queryCityWeather('current', 'London'))