import plotly
import plotly.graph_objs as go
import pandas as pd
import sqlite3

db_con = sqlite3.connect('gr-covid.db')
regions = ['ΖΑΚΥΝΘΟΥ', 'ΘΕΣΣΑΛΟΝΙΚΗΣ']

dataz = pd.read_sql_query("select * from summary ", db_con)
print(dataz)

subset = dataz[dataz['dt'] == "2021-01-01"]
#subset = dataz[dataz['region'].isin(regions)]
subset = dataz[dataz['region'] == "ΖΑΚΥΝΘΟΥ"]#"ΘΕΣΣΑΛΟΝΙΚΗΣ"]
print(subset)


plotly.offline.plot({
    "data": [go.Bar (x = subset['dt'], y = subset['cases'])],
        "layout": go.Layout(title="Coronavirus Cases in ΖΑΚΥΝΘΟΥ")#ΘΕΣΣΑΛΟΝΙΚΗΣ")
})

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
