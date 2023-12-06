import plotly.express as px
import pandas as pd
import json
import numpy as np
import os, sys
import json

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
absolute_directory = os.path.dirname(parent_directory)
sys.path.append(absolute_directory)
sys.path.append(absolute_directory + "/ExternalConnections/api")

from ExternalConnections.api.apiHandler import ApiHandler
from DataHandler import DataHandler as DataHandler

#TODO refactor code to dataHandler be a separate class
class DataPlotter:
    def __init__(self):
        #self.data = None
        # self.apiHandler = ApiHandler()
        # self.dataHandler = DataHandler(self.apiHandler)
        self.data = json.load(open('../Services/DataPlot/data.json'))


    def set_data(self, query_type: str, query_place):
        self.data = self.apiHandler.queryCityWeather(query_type, query_place)

    def _get_day_temperatures(self) -> pd.DataFrame:
        dt, temp = list(), list()
        for dc in self.data['forecast']['forecastday'][0]['hour']:
            dt.append(dc['time'])
            temp.append(dc['temp_c'])
        dt, temp = pd.Series(dt), pd.Series(temp)
        return pd.DataFrame({'Datetime': dt, 'Temp(Celsius)': temp})

    def create_plot(self, selected_column: str, selected_plot_type: str = 'line'):
        df = self._get_day_temperatures()
        match selected_plot_type:
            case "histogram":
                fig = px.histogram(df, x='Datetime', y=selected_column, title=f'Plot of {selected_column}')
            case "scatter":
                fig = px.scatter(df, x='Datetime', y=df[selected_column], title=f'Plot of {selected_column}')
            case "line":
                fig = px.line(df, x='Datetime', y=df[selected_column], title=f'plot type {selected_plot_type}')
            case _:
                raise Exception("Invalid selected_plot_type")
        return fig




# campinas = DataPlotter()
# campinas.data = data
# campinas.create_plot('Temp(Celsius)').show()

