#Basics Requirements
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

#Recall app
from app import app
from lib import stats, benchmark



tab_bar = html.Div(className="tab-bar",
    children=[
        dbc.Tabs(
            [
                dbc.Tab(label="General", tab_id="tab-1"),
                dbc.Tab(label="Stats", tab_id="tab-2"),
                dbc.Tab(label="Clustering", tab_id="tab-3"),
                dbc.Tab(label="Benchmark", tab_id="tab-4"),
                dbc.Tab(label="Principal Insights", tab_id="tab-5"),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="content"),
    ]
)


@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return html.P('Tab1')
    elif at == "tab-2":
        return stats.map
    elif at == "tab-3":
        return html.P('Tab3')
    elif at == "tab-4":
        return benchmark.benchmark
    elif at == "tab-5":
        return html.P('Tab5')
    return html.P("This shouldn't ever be displayed...")