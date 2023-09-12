import plotly.express as px
import pandas as pd
import json
import numpy as np





def parseColumnJSON(json_file, column: str):
    '''
    Retorna um dataframe com colunas dt e column
    '''
    data = json.load(open(json_file))
    df = pd.DataFrame(data['list'])

    df2 = pd.DataFrame({'dt': df['dt']})

    df2[column] = np.zeros(df.shape[0])
    for i in range(df2.shape[0]):
        df2[column][i] = (df['main'][i][column])

    return df2

def create_plot(json_file, selected_column: str, selected_plot_type: str):
    df2 = parseColumnJSON(json_file, selected_column)
    match selected_plot_type:
        case "histogram":
            fig = px.histogram(df2, x='dt', y=df2[selected_column], title=f'Plot of {selected_column}')
        case "scatter":
            fig = px.scatter(df2, x='dt', y=df2[selected_column], title=f'Plot of {selected_column}')
        case _:
            if selected_plot_type is None:
                fig = px.line(df2, x='dt', y=df2[selected_column], title=f'plot type ta none')
            else:
                fig = px.line(df2, x='dt', y=df2[selected_column], title=f'plot type {selected_plot_type}')
    return fig

if __name__ == '__main__':
    fig = create_plot('forecastCampinas.json','temp', 'scatter')
    fig.show()
