import plotly.express as px
import pandas as pd
import json
import numpy as np



def create_plot(selected_column: str, selected_plot_type: str):
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
    data = json.load(open('forecastCampinas.json'))

    df = pd.DataFrame(data['list'])
    print(df)


    df2 = pd.DataFrame({'dt': df['dt']})
    df2['temp'] = np.zeros(df.shape[0])
    for i in range(df2.shape[0]):
        df2['temp'][i] = (df['main'][i]['temp'])
    print(df2)
    
    fig = create_plot('temp' , 'histogram')
    fig.show()