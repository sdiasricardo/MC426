import os, sys, shutil
import pandas as pd

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
absolute_directory = os.path.dirname(parent_directory)
sys.path.append(absolute_directory)
sys.path.append(absolute_directory + "/Services/DataPlot/")

from DataAdapter import DataAdapter
from datetime import datetime
from ExternalConnections.api.geolocator import Geolocator

class DataProcessor:
    def __init__(self, api_caller):
        self.data = None
        self.dataAdapter = DataAdapter(api_caller)

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

    def _build_info_col(self, column : list, day: int, info: str):
        match info:
            case 'Temp °C':
                for hour_idx in range(24):
                    column.append(self.data['forecast']['forecastday'][day]['hour'][hour_idx]['temp_c'])
                return column
            case 'Chuva %':
                for hour_idx in range(24):
                    column.append(self.data['forecast']['forecastday'][day]['hour'][hour_idx]['chance_of_rain'])
                return column
            case _:
                raise Exception('info not matched')
            
    def get_df(self, query: str, day: str, info: str):
        self._set_data(query)
        date_range = pd.date_range('00:00', '23:00', freq='H')
        hours_series = pd.Series(date_range.strftime('%H:%M'))
        dayIndex = self._get_day_index(day)
        return pd.DataFrame({'Hora': hours_series, info: pd.Series(self._build_info_col([], dayIndex, info))})

    def get_general_info(self, query: str, day: str):
        self._set_data(query)
        print(self.data)
        dayIndex = self._get_day_index(day)
        info = dict()
        info['cidade'] = query
        info['temp'] = self.data['current']['temp_c']
        info['chuva'] = self.data['current']['precip_mm']
        info['icone'] = self.data['current']['condition']['icon']
        return info

    def get_geolocator_info(self):
        current_place = Geolocator.get_current_location()
        date_today = str(datetime.today()).split(' ')[0]
        return self.get_general_info(current_place, date_today)

    def get_alerts(self, query: str):
        self._set_data(query)
        return self.data['alerts']['alert']
    
if __name__ == '__main__':
    processor = DataProcessor()
    processor.get_general_info('Campinas', '2023-12-11')


