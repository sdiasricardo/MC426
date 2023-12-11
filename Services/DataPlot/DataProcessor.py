import os, sys, shutil
import pandas as pd

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
absolute_directory = os.path.dirname(parent_directory)
sys.path.append(absolute_directory)
sys.path.append(absolute_directory + "/Services/DataPlot/")

from DataAdapter import DataAdapter
from datetime import datetime, timedelta

class DataProcessor:
    def __init__(self):
        self.data = None
        self.dataAdapter = DataAdapter()

    @staticmethod
    def clear_cache():
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

    def _set_data(self, query: str):
        self.data = self.dataAdapter.get_data(query)

    def _get_day_index(self, expected_day: str):
        '''
        expected_day: str = 'YYYY-MM-DD'
        '''
        date_format = '%Y-%m-%d'
        final_day = datetime.strptime(expected_day, date_format)
        start_day = datetime.today()
        time_difference = final_day - start_day
        number_of_days = time_difference.days + 1
        return number_of_days

    def get_df(self, query: str, day: str, info: str):
        self._set_data(query)
        date_range = pd.date_range('00:00', '23:00', freq='H')
        hours_series = pd.Series(date_range.strftime('%H:%M'))
        dayIndex = self._get_day_index(day)
        info_col = list()
        match info:
            case 'temp':
                for i in range(24):
                    info_col.append(self.data['forecast']['forecastday'][dayIndex]['hour'][i]['temp_c'])
                return pd.DataFrame({'Hours': hours_series, 'Temp (°C)': pd.Series(info_col)})
            case 'rain':
                for i in range(24):
                    info_col.append(self.data['forecast']['forecastday'][dayIndex]['hour'][i]['chance_of_rain'])
                return pd.DataFrame({'Hours': hours_series, 'Chuva %': pd.Series(info_col)})
            case _:
                raise Exception('info not matched')

    def get_general_info(self, query: str, day: str):
        self._set_data(query)
        dayIndex = self._get_day_index(day)
        info = dict()
        info['cidade'] = self.data['location']['name']
        info['pais'] = self.data['location']['country']
        info['horario'] = self.data['location']['localtime']
        info['icone'] = self.data['forecast']['forecastday'][dayIndex]['day']['condition']['icon']
        info['estado'] = self.data['forecast']['forecastday'][dayIndex]['day']['condition']['text']
        info['chuva'] = self.data['forecast']['forecastday'][dayIndex]['day']['daily_chance_of_rain']
        info['umidade'] = self.data['forecast']['forecastday'][dayIndex]['day']['avghumidity']
        info['vento'] = self.data['forecast']['forecastday'][dayIndex]['day']['maxwind_kph']
        info['temp_min'] = self.data['forecast']['forecastday'][dayIndex]['day']['mintemp_c']
        info['temp_max'] = self.data['forecast']['forecastday'][dayIndex]['day']['maxtemp_c']
        return info


    def get_alerts(self, query: str):
        self._set_data(query)
        return self.data['alerts']['alert']

    def _build_df(self, columns: list):
        dates = pd.Series()
        for col in columns:
            pass

if __name__ == '__main__':
    DataProcessor.clear_cache()

    