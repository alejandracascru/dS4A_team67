# Basics Requirements
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
# Recall app
from app import app
from library.elements_all import sidebar
from library.elements_all import dropdown
from library import def_data

clustering = dbc.Row(
    [
        dbc.Col(html.Div([
            sidebar.sidebar,
        ])),
        dbc.Col(html.Div(dropdown.dropdown_variables)),
        dbc.Col(html.Div(dropdown.dropdown_mun)),
    ],
    no_gutters=True,
    align="center",
)

# benchmark = html.P('Fabio A. Lagos')
