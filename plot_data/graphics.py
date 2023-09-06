import plotly.express as px
import plotly.graph_objects as go



x = [1, 2, 3]
y = [1, 2, 3]

fig = px.area(x=x, y=y)
fig.add_trace(
    go.Scatter(
        mode='markers',
        x=x,
        y=y,
        marker=dict(
            color='LightSkyBlue',
            size=30,
        ),
        showlegend=False
    )
)
fig.show()