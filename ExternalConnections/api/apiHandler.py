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

from DataInterface import DataInterface

load_dotenv()
api_key = os.getenv("weather_api_key")

class ApiHandler(DataInterface):
    def __init__(self):
        super.__init__()

    def queryCityWeather(self, query_type: str, query_place):
        '''
        Parameters:
        query_type: current or forecast
        query_place: string representing a city or a tuple [latitude, longitude]
        '''
        if isinstance(query_place, tuple):
            query_place = str(query_place[0]) + ',' + str(query_place[1])
        base_url = f'http://api.weatherapi.com/v1/{query_type}.json?key={api_key}&q={query_place}&days=7&aqi=no&alerts=yes'
        response = requests.get(base_url)
        if response.status_code == 200:
            self.data = response.json()
        else:
            raise Exception(f'Weather API responded with code {response.status_code}')
        
    def get_alerts(self):
        return self.data['alerts']
    
    def get_week_temp(self):
        days = pd.Series()
        temp_c, temp_f = pd.Series(), pd.Series()
        for day in self.data['forecast']['forecastday']:
        

if __name__ == '__main__':
    teste = ApiHandler()