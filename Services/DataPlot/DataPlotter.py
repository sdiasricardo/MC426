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
from DataAdapter import DataAdapter
from DataProcessor import DataProcessor


class DataPlotter:
    def __init__(self):
        self.dataProcessor = DataProcessor()
        
    def _set_df(self, query: str, day: str, info: str) -> dict | None:
        self.df = self.dataProcessor.get_df(query, day, info)

    def plot_day_temp(self, query, day):
        self._set_df(query, day, 'temp')
        self.df.rename(columns={"info": "Temp °C"}, inplace= True)
        fig = px.area(self.df, x = 'Hours', y = self.df['Temp °C'], title = f'{query}')
        fig.update_layout(yaxis_title = 'Temp °C')
        return fig

    def plot_day_rain(self, query, day):
        self._set_df(query, day, 'rain')
        self.df.rename(columns={'info': 'Chuva %'}, inplace = True)
        fig = px.histogram(self.df, x = 'Hours', y = self.df['Chuva %'], title = f'{query}')
        fig.update_layout(yaxis_title = 'Chuva %')
        fig.update_xaxes(range=[-0.5, 23.5])
        return fig

    def create_plot(self, query: str, info: str, day: str):
        match info:
            case 'temp':
                return self.plot_day_temp(query, day)
            case 'rain':
                return self.plot_day_rain(query, day)
            case _:
                raise Exception('Invalid Info')


if __name__ == '__main__':
    plotter = DataPlotter()
    plotter.create_plot('Berlin', 'temp', '2023-12-12').show()

