import plotly.express as px
import pandas as pd
import json
import numpy as np


def parseMainForecastJSON(json_file: str, column: str) -> pd.DataFrame:
    '''
    Retorna um dataframe com colunas de data e column, sendo
    column um parâmetro 'main' do request para o OpenWeather
    '''
    parameters = ["temp", "feels_like", "temp_min", "temp_max", "pressure", "sea_level", "grnd_level",
                  "humidity", "temp_kf"]
    if column not in parameters:
        raise Exception("Column not existent in 'main' parameters of API request")
    try:
        data = json.load(open(json_file))
    except FileNotFoundError:
        raise Exception("File not found")
    except json.decoder.JSONDecodeError:
        raise Exception("File is not JSON type")
    
    try:
        df = pd.DataFrame(data['list'])
    except KeyError:
        raise Exception(" 'list' JSON parameter not found")

    df2 = pd.DataFrame({'dt': df['dt_txt']})

    df2[column] = np.zeros(df.shape[0])
    
    for i in range(df2.shape[0]):
        df2[column][i] = (df['main'][i][column])

    return df2

def create_plot(json_file: str, selected_column: str, selected_plot_type: str = 'line'):
    df2 = parseMainForecastJSON(json_file, selected_column)
    match selected_plot_type:
        case "histogram":
            fig = px.histogram(df2, x='dt', y=selected_column, title=f'Plot of {selected_column}')
        case "scatter":
            fig = px.scatter(df2, x='dt', y=df2[selected_column], title=f'Plot of {selected_column}')
        case "line":
            fig = px.line(df2, x='dt', y=df2[selected_column], title=f'plot type {selected_plot_type}')
        case _:
            raise Exception("Invalid selected_plot_type")
    return fig


if __name__ == '__main__':
    fig = create_plot('test/forecastCampinas.json', 'pressure', 'line')
    fig.show()
