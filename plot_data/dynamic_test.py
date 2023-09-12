from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Country's key performance analytics"),
    html.P("Select data on y-axis:"),
    dcc.Dropdown(
        id='y-axis',
        options=['lifeExp', 'pop', 'gdpPercap'],
        value='gdpPercap'
    ),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"), 
    Input("y-axis", "value"))
def display_area(y):
    df = px.data.gapminder() # replace with your own data source
    countries = (
        df.country.drop_duplicates()
        .sample(n=10, random_state=42)
    )
    df = df[df.country.isin(countries)]

    fig = px.area(
        x="year", y=y,
        color="continent", line_group="country")

    fig.add_trace(
    go.Scatter(
        df,
        x="year",
        y=y,
        mode='markers',
        marker=dict(
            color='LightSkyBlue',
            size=30,
        ),
        showlegend=False
    )
)

    return fig

app.run_server(debug=True)