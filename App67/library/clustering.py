# Basics Requirements
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
# Recall app
from app import app
from library.elements_all import sidebar_benchmarking
from library.elements_all import dropdown
from library import def_data

df_desertion_dept = def_data.runQuery(
    """
    select name_dept, max(desertion_perc) as desertion_perc, max(desertion_no) as desertion_no
    from desertion_by_municip
    group by name_dept
    ;"""
)

clustering = dbc.Row(
    [
        dbc.Col(html.Div([
            sidebar_benchmarking.sidebar,
        ])),
        dbc.Col(html.Div(dropdown.dropdown_mun)),
        dbc.Col(html.Div(dcc.Graph(id='chart'))),
    ],
    no_gutters=True,
    align="center",
)


@app.callback(
    Output('chart', 'figure'),
    [Input('dropdown_mun', 'value')]
)
def build_chart(dropdown_mun):
    dff = df_desertion_dept[df_desertion_dept['name_dept'] == dropdown_mun]
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(dff.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[dff.name_dept, dff.desertion_perc, dff.desertion_no],
                   fill_color='lavender',
                   align='left'))
    ])
    return fig
