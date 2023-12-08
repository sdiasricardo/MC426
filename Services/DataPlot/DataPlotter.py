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
from DataAdapter import DataAdapter
from DataProcessor import DataProcessor
import DataHandler

class DataPlotter:
    def __init__(self):
        self.df = None
        self.dataProcessor = DataProcessor()
        
    def _set_df(self, query: str, day: str, info: str) -> dict | None:
        self.df = self.dataProcessor.get_df(query, day, info)

    def plot_day_temp(self, query, day):
        self._set_df(query, day, 'temp')
        fig = px.area(self.df, x = 'Hours', y = self.df['Temp (°C)'], title = f'{query}')
        return fig

    def plot_day_rain(self, query, day):
        self._set_df(query, day, 'rain')
        fig = px.histogram(self.df, x = 'Hours', y = self.df['Chuva %'], title = f'{query}')
        fig.update_xaxes(range=[-0.5, 23.5])
        return fig

    def create_plot(self, query: str, info: str, day: str):
        self._set_df(query, day, info)
        match info:
            case 'temp':
                return self.plot_day_temp(query, day)
            case 'rain':
                print(self.df)
                return self.plot_day_rain(query, day)
            case _:
                raise Exception('Invalid Info')


if __name__ == '__main__':
    plotter = DataPlotter()
    plotter.create_plot('Paris', 'rain', '2023-12-12').show()

