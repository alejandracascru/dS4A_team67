import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np

import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go

from library.elements_all import sidebar_statistics
from app import app

import plotly.express as px
from plotly.subplots import make_subplots

##############################
# Load Data
##############################
df_all = pd.read_csv('data/df_all.csv')


def get_desercion_variables(df_in, year, in_mun_code):
    df_filtered = df_in[df_in['code_municip'] == in_mun_code]
    df_year = df_filtered[df_filtered['year_cohort'] == year]

    # desercion
    tempval = df_year['desertion_perc'].to_numpy()[0]
    value_desercion = str(np.round(tempval, 2)) + ' %'
    y_plot = df_year[[
        'me_desercion_transicion',
        'me_desercion_primaria',
        'me_desercion_media',
        'me_desercion_secundaria',
    ]].to_numpy()

    derc_perc = [np.round(x * tempval / sum(y_plot[0]), 2) for x in y_plot[0]]

    return value_desercion, derc_perc


def get_cobertura_variables(df_in, year, in_mun_code):
    df_filtered = df_in[df_in['code_municip'] == in_mun_code]
    df_year = df_filtered[df_filtered['year_cohort'] == year]
    # cobertura
    tempval_2 = df_year['me_cobertura_neta'].to_numpy()[0]
    value_cobertura = str(np.round(tempval_2, 2)) + ' %'
    y_plot_2 = df_year[[
        'me_cobertura_neta_transicion',
        'me_cobertura_neta_primaria',
        'me_cobertura_neta_media',
        'me_cobertura_neta_secundaria',
    ]].to_numpy()
    cob_perc = y_plot_2[0]
    return value_cobertura, cob_perc


def get_correlation_df(df_in, var1, var2, year):
    df_year = df_in[df_in['year_cohort'] == year]
    df_out = df_year[[var1, var2, 'name_dept', 'code_dept', 'name_municip', 'code_municip', 'region']]

    region_to_number = {
        'Andina':1,
        'Caribe':2,
        'Amazonica':3,
        'Pacifica':4,
        'Orinoquia':5,
    }

    def change_to_code(region):
        return region_to_number[region]

    new_code = df_out['region'].apply(change_to_code)
    df_out = df_out.assign(reg_code=new_code)
    return df_out


##############################
# Figures
##############################

def make_donut_desertion_fig(label_desercion, derc_perc):
    labels = ['Transición', 'Primaria', 'Media', 'Secundaria']
    fig = go.Figure(data=[go.Pie(labels=labels,
                                 values=derc_perc,
                                 hole=.5,
                                 hoverinfo="label+value"
                                 )
                                 ])
    fig.update_layout(title_text="Deserción Total Población Escolar: " + label_desercion)
    return fig


def make_bar_cobertura_fig(value_cobertura, cob_perc):
    labels = ['Transición', 'Primaria', 'Media', 'Secundaria']
    fig = go.Figure(data=[go.Bar(x=labels,
                                 y=cob_perc,
                                 )])
    fig.update_layout(title_text="Cobertura Total Población Escolar: " + value_cobertura)
    return fig


def figure_desertion_year(df_all, selected_code):
    df_mun = df_all[df_all['code_municip'] == selected_code]
    result_fig = go.Figure(data=go.Scatter(x=df_mun['year_cohort'],
                                           y=df_mun['desertion_perc']
                                           ),
                           )

    result_fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    result_fig.update_layout(title_text="Deserción 2011-2019")

    return result_fig


# def figure_correlation(scatter_df, var1, var2, filter_type='region'):
#     result_fig = go.Figure()
#
#     if filter_type == 'region':
#         filter_selection = 'reg_code'
#     else:
#         filter_selection = 'code_dept'
#
#     regions = scatter_df[filter_selection].unique()
#
#     for r in regions:
#         temp_df = scatter_df[scatter_df[filter_selection] == r]
#         result_fig.add_trace(go.Scatter(
#             x=temp_df[var1],
#             y=temp_df[var2],
#             text=temp_df['region'] + ' - ' + temp_df['name_dept'] + ' - ' + temp_df['name_municip'],
#             name=str(r),
#             mode='markers',
#             marker=dict(
#                 size=16,
#             )
#         ))
#
#     result_fig.update_layout(title='Correlation Selected Variables')
#     return result_fig


##############################
# Call Figures
##############################
selected_code = 5001
selected_year = 2019

df_mun = df_all[df_all['code_municip'] == selected_code]
name_municipio = df_mun.iloc[[0]]['name_dept'].to_numpy()
name_depto = df_mun.iloc[[0]]['name_municip'].to_numpy()

var1_in = 'desertion_perc'
var2_in = 'me_tasa_matriculacion_5_16'

# Pie Figure
label_desercion_in, derc_perc_in = get_desercion_variables(
    df_in=df_all,
    year=selected_year,
    in_mun_code=selected_code,
)

PieFig = make_donut_desertion_fig(
    label_desercion=label_desercion_in,
    derc_perc=derc_perc_in,
)

# Cobertura Figure
value_cobertura_in, cob_perc_in = get_cobertura_variables(
    df_in=df_all,
    year=selected_year,
    in_mun_code=selected_code,
)

BarFig = make_bar_cobertura_fig(
    cob_perc=cob_perc_in,
    value_cobertura=value_cobertura_in
)

# Years figure
Years_fig = figure_desertion_year(
    df_all=df_all,
    selected_code=selected_code
)

# Correlation Figure
# df_scatter = get_correlation_df(
#     df_in=df_all,
#     var1=var1_in,
#     var2=var2_in,
#     year=selected_year
# )
#
# Corr_fig = figure_correlation(
#     scatter_df=df_scatter,
#     var1=var1_in,
#     var2=var2_in,
#     filter_type='region'
# )

##############################
# Dropdowns
##############################

dropdown_region = dcc.Dropdown(
    id='demo-dropdown',
    options=[
        {'label': 'Regiones', 'value': 'region'},
        {'label': 'Departamentos', 'value': 'depto'}
    ],
    value='region'
)

##############################
# Layout
##############################

explore_municipio = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H3(""),
                    align="start",
                    width=2
                ),
                dbc.Col(
                    html.H3("Explorar Deserción y Cobertura por Municipio"),
                    align="center",
                ),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    html.Div('Dropdown'), width=2
                ),
                dbc.Col(
                    dcc.Graph(figure=PieFig, id='Pie_d'), width=3
                ),
                dbc.Col(
                    dcc.Graph(figure=Years_fig, id='Years_d'), width=4
                ),
                dbc.Col(
                    dcc.Graph(figure=BarFig, id='Bar_c'), width=3
                ),
            ],
            align="center",
        ),
    ]
)

explore_correlation = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H3(""),
                    align="start",
                    width=2
                ),
                dbc.Col(
                    html.H3("Explorar Correlación entre Variables"),
                    align="start",
                ),
            ]
        ),

        dbc.Row([
            dbc.Col(
                html.Div(""), width=2
            ),
            dbc.Col(
                html.Div("Seleccione Filtro"), width=3
            ),
            dbc.Col(
                html.Div(dropdown_region), width=5
            ),
        ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    html.Div(""), width=1
                ),
                dbc.Col(
                    html.Div(""), width=1
                ),
                dbc.Col(
                    dcc.Graph(id='Corr_fig'), width=12
                ),
            ],
            align="center",
        ),
    ]
)


dbc.Col(html.Div("One of three columns"), width=3),
statistics = html.Div(
    [
        sidebar_statistics.sidebar,
        dbc.Row(html.Div(
            explore_correlation
        ),style={'position':'fixed','left':'17rem'}),

        dbc.Row(dbc.Col(
            html.Div("")
        )),

        dbc.Button(
            "Explorar Deserción y Cobertura por Municipio",
            id="collapse-button",
            className="mb-3",
            color="secondary",
        ),
        dbc.Collapse(
            dbc.Card(dbc.CardBody(
                explore_municipio
            )),
            id="collapse",
        ),

    ]
)


##############################
# Callbacks
##############################


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open



@app.callback(
    Output('Corr_fig', 'figure'),
    [Input('demo-dropdown', 'value')])
def figure_correlation(value):

    var1_in = 'desertion_perc'
    var2_in = 'me_tasa_matriculacion_5_16'

    scatter_df = get_correlation_df(
        df_in=df_all,
        var1=var1_in,
        var2=var2_in,
        year=selected_year
    )

    result_fig = go.Figure()

    if value == 'region':
        filter_selection = 'reg_code'
    else:
        filter_selection = 'code_dept'

    regions = scatter_df[filter_selection].unique()

    for r in regions:
        temp_df = scatter_df[scatter_df[filter_selection] == r]
        result_fig.add_trace(go.Scatter(
            x=temp_df[var1_in],
            y=temp_df[var2_in],
            text=temp_df['region'] + ' - ' + temp_df['name_dept'] + ' - ' + temp_df['name_municip'],
            name=str(r),
            mode='markers',
            marker=dict(
                size=16,
            )
        ))

    result_fig.update_layout(title='Correlation Selected Variables')
    return result_fig

