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
    fig.update_layout(title_text="Total School Population Drop Out: " + label_desercion)
    return fig


def make_bar_cobertura_fig(value_cobertura, cob_perc):
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
        title_text="School Drop Out Percentage vs Years",
        xaxis_title="Year",
        yaxis_title="School Drop Out [%]",
    )

    return result_fig


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

# @app.callback(
#     Output(component_id='test-output', component_property='children'),
#     [Input(f'stats_checklist_{i}', 'value') for i in sidebar_groups],
#     [State(f"stats_collapse-{i}", "is_open") for i in sidebar_groups],
#
# )
# def update_output_div(*args):
#     values = args[0:int(len(args)/2)]
#     is_open = args[int(len(args)/2):]
#     output = ''
#     label = ''
#     for i in range(len(values)):
#         check_vars = values[i]
#         temp_is_open = is_open[i]
#         if check_vars is not None and temp_is_open:
#             output = check_vars
#             label_temp = df_vars_here[df_vars_here['var_id'] == output]['name'].to_numpy()
#             label = str(label_temp[0])
#     return 'Output: {}'.format(label)


@app.callback(
    Output('Corr_fig', 'figure'),
    [Input(f'stats_checklist_{i}', 'value') for i in sidebar_groups],
    [State(f"stats_collapse-{i}", "is_open") for i in sidebar_groups],
)
def figure_correlation(*args):
    # n_args = len(args)
    values = args[0:int(len(args)/2)]
    is_open = args[int(len(args)/2):]

    def selected_var(values, is_open):
        output = ''
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
        else:
            label = 'sa_punt_matematicas'
            axis_l = 'Math Score - National Test'
        return label, axis_l

    var1_in = 'desertion_perc'
    var2_in, var2_l = selected_var(values, is_open)

    scatter_df = get_correlation_df(
        df_in=df_all,
        var1=var1_in,
        var2=var2_in,
        year=selected_year
    )

    result_fig = go.Figure()
    reg_dept = 'dept'
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
            x=temp_df[var1_in],
            y=temp_df[var2_in],
            text=temp_df['region'] + ' - ' + temp_df['name_dept'] + ' - ' + temp_df['name_municip'],
            name=label_dictionary[str(r)],
            mode='markers',
            marker=dict(
                size=16,
            )
        ))

    result_fig.update_layout(
        title='Correlation Selected Variables',
        xaxis_title="School Drop Out Percentage [%]",
        yaxis_title=var2_l,
    )
    return result_fig


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
                    html.H3("Municipality Statistics", style={"left": "10px"}),
                ),
            ]
        ),

        dbc.Row(
            [
                dbc.Row(
                    dcc.Graph(figure=Years_fig, id='Years_d'),
                ),
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(figure=PieFig, id='Pie_d'),
                    ),
                    dbc.Col(
                        dcc.Graph(figure=BarFig, id='Bar_c'),
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

        dbc.Row(
            dcc.Graph(id='Corr_fig'),
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

                dbc.Row(explore_correlation),

                dbc.Button(
                        "Explore Municipality Statistics",
                        id="collapse-button",
                        className="mb-3",
                        color="secondary",
                ),

                dbc.Collapse(
                    dbc.Card(dbc.CardBody(
                        explore_municipio,
                    )),
                    id="collapse",
                ),

            ], style={'position': 'absolute', 'left': '20rem', 'top': '11rem', "width": "75%"}
        ),

    ]
)
