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
    
    def create_plot(self, query: str, info: str, day: str):
        self._set_df(query, day, info)
        match info:
            case 'Temp °C':
                fig = px.area(self.df, x = 'Hora', y = self.df['Temp °C'], title = f'{query}')
            case 'Chuva %':
                fig = px.bar(self.df, x='Hora', y='Chuva %', title=f'{query}')
                fig.update_traces(texttemplate='%{y}', textposition='outside')
                fig.update_xaxes(range=[-0.5, 23.5])
            case _:
                raise Exception('Invalid Info')
        return fig


if __name__ == '__main__':
    plotter = DataPlotter()
    plotter.create_plot('Berlin', 'Chuva %', '2023-12-12').show()

