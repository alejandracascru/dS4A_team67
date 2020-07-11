"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from urllib.request import urlopen
import json
import plotly.express as px
from .data import create_dataframe, create_icbf_dataframe, create_desertion_dataframe
from .layout import html_layout


def create_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/dist/css/styles.css',
            'https://fonts.googleapis.com/css?family=Lato'
        ]
    )

    # Load DataFrame
    df = create_dataframe()
    df_icbf = create_icbf_dataframe()
    df_desertion = create_desertion_dataframe()

    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = html.Div(
        children=[dcc.Graph(
            id='histogram-graph',
            figure={
                'data': [{
                    'x': df['complaint_type'],
                    'text': df['complaint_type'],
                    'customdata': df['key'],
                    'name': '311 Calls by region.',
                    'type': 'histogram'
                }],
                'layout': {
                    'title': 'NYC 311 Calls category.',
                    'height': 500,
                    'padding': 150
                }
            }),
            create_data_table(df_icbf),
            dcc.Graph(figure=create_map(df_desertion))
            #create_map(df_desertion)
        ],
        id='dash-container'
    )
    return dash_app.server


def create_data_table(df):
    """Create Dash datatable from Pandas DataFrame."""
    table = dash_table.DataTable(
        id='database-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        sort_action="native",
        sort_mode='native',
        page_size=50
    )
    return table


def create_map(df):
    # Read the geojson file for Colombian Departments
    with urlopen(
            'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw'
            '/3aadedf47badbdac823b00dbe259f6bc6d9e1899/colombia.geo.json') as response:
        depts = json.load(response)
    for loc in depts['features']:
        loc['id'] = loc['properties']['DPTO']

    dep_map = px.choropleth_mapbox(df, geojson=depts, locations='code_dept', color='desertion',
                                   color_continuous_scale="Viridis",
                                   range_color=(1, 7),
                                   mapbox_style="carto-positron",
                                   zoom=4, center={"lat": 4.670128, "lon": -74.047078},
                                   opacity=0.5,
                                   labels={'desertion': 'desertion rate'}
                                   )
    dep_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return dep_map
