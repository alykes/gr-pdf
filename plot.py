import plotly
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from plotly.subplots import make_subplots



db_con = sqlite3.connect('gr-covid.db')
regions = ['ΖΑΚΥΝΘΟΥ', 'ΘΕΣΣΑΛΟΝΙΚΗΣ']

dataz = pd.read_sql_query("select * from summary ", db_con)
print(dataz)

datez = "2021-01-01"
subset = dataz[dataz['dt'] == datez]
#subset = dataz[dataz['region'].isin(regions)]
subset_zante = dataz[dataz['region'] == "ΖΑΚΥΝΘΟΥ"]#"ΘΕΣΣΑΛΟΝΙΚΗΣ"]
subset_thess = dataz[dataz['region'] == "ΘΕΣΣΑΛΟΝΙΚΗΣ"]
print(subset)


fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_bar(
    secondary_y = False,
    x = subset_zante['dt'],
    y = subset_zante['cases'],
    marker_color = "SkyBlue",
    name = "ΖΑΚΥΝΘΟΥ")

fig.update_yaxes(
    secondary_y = False,
    tickfont_color = "SkyBlue",
    title = "Cases per Day")

# fig.add_scatter(secondary_y=True,  x=subset_thess['dt'], y = subset_thess['cases'],
#                 marker_color="DarkOrange", name="ΘΕΣΣΑΛΟΝΙΚΗΣ")
fig.add_scatter(
    secondary_y = True,
    x=subset_zante['dt'],
    y = subset_zante['avg7day'],
    marker_color="RebeccaPurple",
    name = "7 Day Average")

# fig.update_yaxes(secondary_y=True,
#                 tickfont_color="DarkOrange", title="Cases")
fig.update_yaxes(
    secondary_y=True,
    tickfont_color="RebeccaPurple",
    title="7 Day Average")

fig.update_yaxes(
    scaleratio = 1,
    range=[0,30])

fig.update_layout(title_text="COVID-19 cases in Zakynthos (Greece) from the 1st Jan 2021")
fig.show()


plotly.io.write_html(fig, "stats.html")


# fig = plotly.offline.plot({
#     "data": [go.Bar (x = subset_zante['dt'], y = subset_zante['cases'])],
#         "layout": go.Layout(title="Coronavirus Cases in ΖΑΚΥΝΘΟΥ")#ΘΕΣΣΑΛΟΝΙΚΗΣ")
# })

# from plotly.subplots import make_subplots
# fig = make_subplots(rows=2, cols=2,
#                     specs=[[{"type": "xy"}, {"type": "polar"}],
#                            [{"type": "domain"}, {"type": "scene"}]])
# fig.add_bar(row=1, col=1, y=[2, 3, 1], )
# fig.add_pie(row=2, col=1, values=[2, 3, 1])
# fig.add_barpolar(row=1, col=2, theta=[0, 45, 90], r=[2, 3, 1])
# fig.add_scatter3d(row=2, col=2, x=[2, 3], y=[0, 0], z=[0.5, 1])
# fig.update_layout(height=700, showlegend=False)
# fig.show()

#
# fig.update_xaxes(
#     rangeslider_visible=True,
#     rangeselector=dict(
#         buttons=list([
#             dict(count=1, label="1m", step="month", stepmode="backward"),
#             dict(count=6, label="6m", step="month", stepmode="backward"),
#             dict(count=1, label="YTD", step="year", stepmode="todate"),
#             dict(count=1, label="1y", step="year", stepmode="backward"),
#             dict(step="all")
#         ])
#     )
# )
#
# fig.show()


# plotly.offline.plot({
#     "data": [go.Bar(x=['Mario', 'Luigi', 'Bowser', 'Toad', 'Peach', 'Koopa'], y=[6, 5, 1, 4, 3, 2])],
#         "layout": go.Layout(title="Super Mario Character Ratings")
# 	}, auto_open=True)

# data  = go.Data([
#             go.Bar(
#               y = dataz.cases,
#               x = dataz.region,
#               orientation='h'
#         )])
# layout = go.Layout(
#         height = '1000',
#         margin=go.Margin(l=300),
#         title = "Coronavirus Cases in Greece"
# )
#
# fig  = go.Figure(data=data, layout=layout)
# py.iplot(fig)
