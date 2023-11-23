import requests
import os
#TODO: Colocar dotenv como dependencia do projeto
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.getenv("weather_api_key")

class ApiHandler:
    def __init__(self) -> None:
        pass

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
            return response.json()
        else:
            raise Exception(f'Weather API responded with code {response.status_code}')