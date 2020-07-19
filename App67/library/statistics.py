import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

##############################
# Load Data
##############################
df_all = pd.read_csv('data/df_all.csv')


def get_summary_variables(df_in, year, in_mun_code):
    df_filtered = df_in[df_in['code_municip'] == in_mun_code]
    df_year = df_filtered[df_filtered['year_cohort'] == year]

    # desercion
    tempval = df_year['desertion_perc'].to_numpy()[0]
    label_desercion = str(np.round(tempval, 2)) + ' %'
    y_plot = df_year[[
        'me_desercion_transicion',
        'me_desercion_primaria',
        'me_desercion_media',
        'me_desercion_secundaria',
    ]].to_numpy()

    derc_perc = [x * tempval / sum(y_plot[0]) for x in y_plot[0]]

    # cobertura
    tempval_2 = df_year['me_cobertura_neta'].to_numpy()[0]
    label_cobertura = str(np.round(tempval_2, 2)) + ' %'
    y_plot_2 = df_year[[
        'me_cobertura_neta_transicion',
        'me_cobertura_neta_primaria',
        'me_cobertura_neta_media',
        'me_cobertura_neta_secundaria',
    ]].to_numpy()

    cob_perc = [x * tempval_2 / sum(y_plot_2[0]) for x in y_plot_2[0]]
    return label_desercion, derc_perc, label_cobertura, cob_perc


def make_summary_fig(name_municipio,  name_depto, year, label_desercion, derc_perc, label_cobertura, cob_perc):
    labels = ['Transición', 'Primaria', 'Media', 'Secundaria']
    sum_fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    sum_fig.add_trace(go.Pie(labels=labels, values=derc_perc, name="Desercion",
                             title="Deserción:" + label_desercion), 1, 1)
    sum_fig.add_trace(go.Pie(labels=labels, values=cob_perc, name="Aprobacion",
                             title='Cobertura:' + label_cobertura), 1, 2)

    # donut-like pie chart
    sum_fig.update_traces(hole=.4, hoverinfo="label+percent+name")
    sum_fig.update_layout(
        title_text="Deserción y Cobertura Escolar - " + str(year) + ' - ' + name_municipio[0] + ' - ' + name_depto[0])
    return sum_fig


def figure_desertion_year(df_all, selected_code, name_municipio):
    df_mun = df_all[df_all['code_municip'] == selected_code]
    result_fig = go.Figure(data=go.Scatter(x=df_mun['year_cohort'],
                                           y=df_mun['desertion_perc']
                                           ))
    return result_fig


##### Call Figures

selected_code = 5001
selected_year = 2019

label_desercion, derc_perc, label_cobertura, cob_perc = get_summary_variables(df_in=df_all,
                                                                              year=2019,
                                                                              in_mun_code=selected_code,
                                                                              )

df_mun = df_all[df_all['code_municip'] == selected_code]
name_municipio = df_mun.iloc[[0]]['name_dept'].to_numpy()
name_depto = df_mun.iloc[[0]]['name_municip'].to_numpy()

Summary_Fig = make_summary_fig(name_municipio=name_municipio,
                               name_depto=name_depto,
                               year=selected_year,
                               label_desercion=label_desercion,
                               derc_perc=derc_perc,
                               label_cobertura=label_cobertura,
                               cob_perc=cob_perc)

Years_fig = figure_desertion_year(df_all, selected_code, name_municipio)

##############################
#Map Layout
##############################
statistics = html.Div([
    dcc.Graph(figure=Summary_Fig, id='summary-figure'),
    dcc.Graph(figure=Years_fig, id='year-figure'),
], className="ds4a-body")