import pandas as pd
from sqlalchemy import create_engine, text
import os
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
from urllib.request import urlopen
import json

#Load data from AWS RDB
DB_USERNAME = 'datateam'
DB_PASSWORD = 'ds4a'
DB_ENDPOINT = 'ds4a-instance.ceogize7tpta.us-east-2.rds.amazonaws.com'
DB_NAME = 'desertion'
engine=create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_ENDPOINT}/{DB_NAME}', max_overflow=20)

def runQuery(sql):
    result = engine.connect().execution_options(isolation_level="AUTOCOMMIT").execute((text(sql)))
    return pd.DataFrame(result.fetchall(), columns=result.keys())

#Query the data from RDB
df_test = runQuery("""
select department, LPAD(cod_dept::text, 2, '0') as cod_dept, desertion 
from des_dep
where year = 2019
;""")

#Define figures and graphs
fig = px.bar(df_test, x="department", y="desertion")

#Read the geojson file for Colombian Departments
with urlopen('https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/3aadedf47badbdac823b00dbe259f6bc6d9e1899/colombia.geo.json') as response:
    depts = json.load(response)
for loc in depts['features']:
    loc['id'] = loc['properties']['DPTO']
#depts = json.load('col.geo.json')

#Colombian map

dep_map = px.choropleth_mapbox(df_test, geojson=depts, locations='cod_dept', color='desertion',
                           color_continuous_scale="Viridis",
                           range_color=(1, 7),
                           mapbox_style="carto-positron",
                           zoom=4, center = {"lat": 4.670128, "lon": -74.047078},
                           opacity=0.5,
                           labels={'desertion':'desertion rate'}
                          )
dep_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

#Dash App
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("Deserción Escolar en Colombia"),
        html.Hr(),
        #dbc.Button(
        #    "Regenerate graphs",
        #    color="primary",
        #    block=True,
        #    id="button",
        #    className="mb-3",
        #),
        #Define Tabs
        dbc.Tabs(
            [
                dbc.Tab(label="Mapas", tab_id="maps"),
                dbc.Tab(label="Estadisticas", tab_id="stats"),
                dbc.Tab(label="Clustering", tab_id="cluster"),
            ],
            id="tabs",
            active_tab="maps",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)

#Callback for the tabs
@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")],
)
def render_tab_content(active_tab, data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab :
        if active_tab == "maps":
            return dcc.Graph(figure=dep_map)
        elif active_tab == "stats":
            return dcc.Graph(figure=fig) #This shows the figure defined previously
        elif active_tab == 'cluster':
            return dcc.Graph(figure=data["cluster"])
    return "No tab selected"


if __name__ == '__main__':
    app.run_server(debug=True,host = '127.0.0.1')