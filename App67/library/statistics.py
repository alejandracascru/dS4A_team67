import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np

import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go

from library import def_data
from library.elements_all import sidebar_statistics
from app import app

import plotly.express as px
from plotly.subplots import make_subplots

##############################
# 1. Load Data
##############################

df_all = pd.read_csv('data/df_all_3.csv')
df_all = df_all.sort_values(by=['code_municip', 'year_cohort'])

var_x_in = 'sa_punt_matematicas'
var_x_l = 'National Test - Saber Pro Score'
var_y_in = 'desertion_perc'
var_y_l = 'School Desertion Percentage [%]'


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
        'Andina':'1',
        'Caribe':'2',
        'Amazonica':'3',
        'Pacifica':'4',
        'Orinoquia':'5',
    }

    def change_to_code(region):
        return region_to_number[region]

    new_code = df_out['region'].apply(change_to_code)
    df_out = df_out.assign(reg_code=new_code)
    return df_out


def get_municipalities(df_in):
    df_names = df_in['name_dept'] + '-' + df_in['name_municip'] + '--' + df_in['code_municip'].apply(str)
    array_names = df_names.unique()
    array_options = []
    for i in array_names:
        array_temp = i.split('--')
        label_temp = array_temp[0]
        value_temp = array_temp[1]
        array_options.append({
            'label': label_temp,
            'value': int(value_temp)})
    return array_options

##############################
# Figures
##############################


def make_donut_desertion_fig(df_in_m, selected_year, selected_code):
    label_desercion, derc_perc = get_desercion_variables(
        df_in=df_in_m,
        year=selected_year,
        in_mun_code=selected_code,
    )

    labels = ['Transición', 'Primaria', 'Media', 'Secundaria']
    fig = go.Figure(data=[go.Pie(labels=labels,
                                 values=derc_perc,
                                 hole=.5,
                                 hoverinfo="label+value"
                                 )
                                 ])
    fig.update_layout(title_text="Total School Population Desertion: " + label_desercion)
    return fig


def make_bar_cobertura_fig(df_in_c, selected_year, selected_code):

    value_cobertura, cob_perc = get_cobertura_variables(
        df_in=df_in_c,
        year=selected_year,
        in_mun_code=selected_code,
    )

    labels = ['Transición', 'Primaria', 'Media', 'Secundaria']
    fig = go.Figure(data=[go.Bar(x=labels,
                                 y=cob_perc,
                                 )])
    fig.update_layout(
        title_text="Total School Population Coverage: " + value_cobertura,
        xaxis_title="Year",
        yaxis_title="School Population Coverage [%]",
    )
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

    result_fig.update_layout(
        title_text="School Desertion Percentage vs Years",
        xaxis_title="Year",
        yaxis_title="School Desertion [%]",
    )

    return result_fig


def figure_cobertura_year(df_all, selected_code):
    df_mun = df_all[df_all['code_municip'] == selected_code]
    result_fig = go.Figure(data=go.Scatter(x=df_mun['year_cohort'],
                                           y=df_mun['me_cobertura_neta']
                                           ),
                           )

    result_fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    result_fig.update_layout(
        title_text="School Population Coverage vs Years",
        xaxis_title="Year",
        yaxis_title="School Population Coverage [%]",
    )

    return result_fig



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


sidebar_groups = sidebar_statistics.df_vars['group_id'].unique()
sidebar_vars = sidebar_statistics.df_vars['var_id'].unique()
df_vars_here = sidebar_statistics.df_vars


@app.callback(
    Output('Corr_fig', 'figure'),
    [
        Input('demo-dropdown', 'value'),
        Input('xy-dropdown', 'value'),
        Input('year-dropdown', 'value'),

        Input('cluster_radio_log_x', 'value'),
        Input('cluster_radio_log_y', 'value'),

        Input('stats_checklist_1', 'value'),
        Input('stats_checklist_2', 'value'),
        Input('stats_checklist_3', 'value'),
        Input('stats_checklist_4', 'value'),
        Input('stats_checklist_5', 'value'),
        Input('stats_checklist_6', 'value'),
        Input('stats_checklist_7', 'value'),
        Input('stats_checklist_8', 'value'),

     ],
    [State(f"stats_collapse-{i}", "is_open") for i in sidebar_groups],
)
def figure_correlation(*args):
    n_groups = len(sidebar_groups)+1
    reg_dept = args[0]
    xy_selection = args[1]
    year_selection = args[2]
    log_value_x = args[3]
    log_value_y = args[4]
    values = args[5:13]
    is_open = args[13:]

    global var_x_in
    global var_x_l
    global var_y_in
    global var_y_l

    log_scale_x = True if log_value_x == 'log' else False
    log_scale_y = True if log_value_y == 'log' else False

    def selected_var(values, is_open):
        output = ''
        correct = False
        for i in range(len(values)):
            check_vars = values[i]
            temp_is_open = is_open[i]
            if check_vars is not None and temp_is_open:
                output = str(check_vars)
        if output != '':
            label_temp = df_vars_here[df_vars_here['var_id'] == output]['name'].to_numpy()
            label = str(label_temp[0])

            axis_temp = df_vars_here[df_vars_here['var_id'] == output]['label'].to_numpy()
            axis_l = str(axis_temp[0])
            correct = True
        return label, axis_l, correct

    if xy_selection == 'x_selected':
        var_x_temp, label_x_temp, correct = selected_var(values, is_open)
        if correct:
            var_x_in = var_x_temp
            var_x_l = label_x_temp
        else:
            var_x_in = 'sa_punt_matematicas'
            var_x_l = 'National Test - Saber Pro Score'

    elif xy_selection == 'y_selected':
        var_y_temp, label_y_temp, correct = selected_var(values, is_open)
        if correct:
            var_y_in = var_y_temp
            var_y_l = label_y_temp
        else:
            var_y_in = 'desertion_perc'
            var_y_l = 'School Desertion Percentage [%]'
    else:
        var_x_in = 'sa_punt_matematicas'
        var_x_l = 'National Test - Saber Pro Score'
        var_y_in = 'desertion_perc'
        var_y_l = 'School Desertion Percentage [%]'


    scatter_df = get_correlation_df(
        df_in=df_all,
        var1=var_x_in,
        var2=var_y_in,
        year=year_selection,
    )

    result_fig = go.Figure()

    if reg_dept == 'region':
        filter_selection = 'reg_code'
        label_dictionary = {
            '1': 'Andina',
            '2': 'Caribe',
            '3': 'Amazonica',
            '4': 'Pacifica',
            '5': 'Orinoquia',
        }
    else:
        filter_selection = 'code_dept'
        label_dictionary = {
            '91': 'Amazonas', '5': 'Antioquia', '81': 'Arauca', '8': 'Atlántico', '11': 'Bogotá D.C.',
            '13': 'Bolívar', '15': 'Boyacá', '17': 'Caldas', '18': 'Caquetá', '85': 'Casanare',
            '19': 'Cauca', '20': 'Cesar', '27': 'Chocó', '23': 'Córdoba', '25': 'Cundinamarca',
            '94': 'Guainía', '95': 'Guaviare', '41': 'Huila', '44': 'La Guajira', '47': 'Magdalena',
            '50': 'Meta', '52': 'Nariño', '54': 'Norte de Santander', '86': 'Putumayo', '63': 'Quindío',
            '66': 'Risaralda', '88': 'San Andrés y Providencia', '68': 'Santander', '70': 'Sucre', '73': 'Tolima',
            '76': 'Valle del Cauca', '97': 'Vaupés', '99': 'Vichada'
        }

    regions = scatter_df[filter_selection].unique()

    for r in regions:
        temp_df = scatter_df[scatter_df[filter_selection] == r]
        result_fig.add_trace(go.Scatter(
            x=temp_df[var_x_in],
            y=temp_df[var_y_in],
            text=temp_df['region'] + ' - ' + temp_df['name_dept'] + ' - ' + temp_df['name_municip'],
            name=label_dictionary[str(r)],
            mode='markers',
            marker=dict(
                size=8,
            )
        ))

    result_fig.update_layout(
        title='Correlation Selected Variables',
        xaxis_title=var_x_l,
        yaxis_title=var_y_l,
    )
    if log_scale_x:
        result_fig.update_xaxes(
            type="log"
        )
    if log_scale_y:
        result_fig.update_yaxes(
            type="log"
        )
    return result_fig


@app.callback(
    Output('years_desertion_fig', 'figure'),
    [
        Input('drop-municipality', 'value'),
     ],
)
def figure_years_desertion(*args):
    code_municip = args[0]
    Years_fig = figure_desertion_year(
        df_all=df_all,
        selected_code=code_municip
    )
    return Years_fig


@app.callback(
    Output('years_cobert_fig', 'figure'),
    [
        Input('drop-municipality', 'value'),
     ],
)
def figure_years_desertion(*args):
    code_municip = args[0]
    fig = figure_cobertura_year(
        df_all=df_all,
        selected_code=code_municip
    )
    return fig


@app.callback(
    Output('Pie_d', 'figure'),
    [
        Input('drop-municipality', 'value'),
        Input('year-dropdown-m', 'value'),
     ],
)
def figure_donut_desertion(*args):
    code_municip = args[0]
    year_municip = args[1]
    fig = make_donut_desertion_fig(
        df_in_m=df_all,
        selected_year=year_municip,
        selected_code=code_municip,

    )
    return fig


@app.callback(
    Output('Bar_c', 'figure'),
    [
        Input('drop-municipality', 'value'),
        Input('year-dropdown-m', 'value'),
     ],
)
def figure_bar_cobertura(*args):
    code_municip = args[0]
    year_municip = args[1]
    fig = make_bar_cobertura_fig(
        df_in_c=df_all,
        selected_year = year_municip,
        selected_code=code_municip
    )
    return fig



##############################
# Dropdowns
##############################

dropdown_region = dcc.Dropdown(
    id='demo-dropdown',
    options=[
        {'label': 'Regions', 'value': 'region'},
        {'label': 'Departments', 'value': 'depto'}
    ],
    value='region'
)

dropdown_municipalities = dcc.Dropdown(
    id='drop-municipality',
    options=get_municipalities(df_all),
    value=5001,
    style={"width": "400px"}
)

cluster_radio_log = dcc.RadioItems(
    options=[
        {'label': '   Linear   ', 'value': 'linear'},
        {'label': '   Log(x)   ', 'value': 'log'}
    ],
    value='linear',
    labelStyle={'display': 'inline-block'},
    id='cluster_radio_log_x'
)

cluster_radio_log_y = dcc.RadioItems(
    options=[
        {'label': '   Linear   ', 'value': 'linear'},
        {'label': '   Log(x)   ', 'value': 'log'}
    ],
    value='linear',
    labelStyle={'display': 'inline-block'},
    id='cluster_radio_log_y'
)

dropdown_years_municipalities = dcc.Dropdown(
    id='year-dropdown-m',
    options=[
        {'label': '2011', 'value': 2011},
        {'label': '2012', 'value': 2012},
        {'label': '2013', 'value': 2013},
        {'label': '2014', 'value': 2014},
        {'label': '2015', 'value': 2015},
        {'label': '2016', 'value': 2016},
        {'label': '2017', 'value': 2017},
        {'label': '2018', 'value': 2018},
        {'label': '2019', 'value': 2019},

    ],
    value=2019,
    style={"width": "300px"}
)


##############################
# Layout
##############################
GROUP_TABLE_BENCHMARK_STYLE = {
        "position": "fixed",
        "width": "20%",
        "right": "1rem",
        "top": "140px",
        "border": "1px solid #e7eff6",
        "border-radius": "10px"
    }


explore_municipio = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H3("Municipality Statistics", style={"left": "40px"}),
                ),
            ]
        ),

        dbc.Row(html.Div(html.Br())),

        dbc.Row([
            dbc.Col(
                html.Div("Select Municipality",  style={"width": "200px"}), width=2
            ),
            dbc.Col(
                dropdown_municipalities,
            ),
        ]
        ),

        dbc.Row(
            [
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(id='years_cobert_fig'),
                    ),
                    dbc.Col(
                        dcc.Graph(id='years_desertion_fig'),
                    ),
                ]),

                dbc.Row(html.Div(html.Br())),

                dbc.Row([
                    dbc.Col(
                        html.Div("Explore Details for Year"), style={"left": "30px", "width": "200px", "text-align": "center"},
                    ),
                    dbc.Col(
                        dropdown_years_municipalities, style={"left": "100px", "width": "300px"}
                    ),
                ]
                ),
                dbc.Row(html.Div(html.Br())),

                dbc.Row([
                    dbc.Col(
                        dcc.Graph(id='Bar_c'),
                    ),
                    dbc.Col(
                        dcc.Graph(id='Pie_d'),
                    ),
                ]),
            ],
        ),
    ]
)

explore_correlation = html.Div(
    [

        dbc.Row([
            dbc.Col(
                html.Div("Select Hue Filter"),
            ),
            dbc.Col(
                html.Div(dropdown_region),
            ),
        ]),

        dbc.Row(html.Div(html.Br())),

        dbc.Row([
            dbc.Col([
                html.Div("Select Scale X-axes"),
                cluster_radio_log,
            ]
            ),
            dbc.Col([
                html.Div("Select Scale Y-axes"),
                cluster_radio_log_y,
            ]
            ),
        ]
        ),


        dbc.Row(
            dcc.Graph(id='Corr_fig'),
            style={"left": "100px", "width": "100%"}
        ),
    ]
)


statistics = html.Div(
    [
        sidebar_statistics.sidebar,

        html.Div(
            [
                html.H3("Explore Variables Correlation",
                    id='test-output',
                    style={"top": "10px"},
                    ),

                dbc.Row(html.Div(html.Br())),

                dbc.Row(explore_correlation),

                dbc.Row(explore_municipio),


            ], style={'position': 'absolute', 'left': '20rem', 'top': '11rem', "width": "75%"}
        ),

    ]
)
