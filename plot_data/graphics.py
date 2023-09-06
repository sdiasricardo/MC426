import plotly.express as px
df = px.data.gapminder()
fig = px.area(df, x="year", y="pop", color="continent", line_group="country")
# fig = px.scatter(df, x="year", y="pop", color="continent")
fig.add_scatter()
fig.show()