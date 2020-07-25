# Basics Requirements
import dash_core_components as dcc
import dash_html_components as html
#import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output, State

import json
import pandas as pd

# Recall app
from app import app
from library.elements_all import sidebar_maps
from library.elements_all import dropdown
from library import def_data


MAP_BENCHMARK_STYLE = {
     "position": "fixed",
     "width": "50%",
     "left": "17rem",
     "top": "140px",
     "border": "1px solid #e7eff6",
 #    "border-radius": "2px"
}

RANKING_TABLE_BENCHMARK_STYLE = {
     "position": "fixed",
     "width": "20%",
     "right": "1rem",
     "top": "140px",
     "border": "1px solid #e7eff6",
     "border-radius": "10px"
}

df_desertion_dept = def_data.runQuery(
     """
     select *
     from master_table_by_municipio
     where year_cohort = 2019
     ;"""
)

dff = df_desertion_dept.copy()


# #############################
# # Load map data
# #############################

with open('data/MGN_MPIO_POLITICO.json') as geo:
     MUN_json = json.loads(geo.read())

with open('data/MGN_DPTO_POLITICO.json') as f:
     DEP_json = json.loads(f.read())

MUN2_json = DEP_json.copy()
fig_geojson = DEP_json


fig = px.choropleth_mapbox(df_desertion_dept, geojson=DEP_json, color="desertion_perc",
                            locations="code_dept", featureidkey="properties.DPTO_CCDGO",
                            color_continuous_scale = "Blues",
                            center={"lat": 4.94, "lon": -73.77},
                            hover_name="name_dept",
                            mapbox_style="carto-positron", zoom=4)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#
# ##############################
# #Call Backs
# ##############################
#@app.callback(
#     Output('maps_fig1', 'figure'),
#     [Input('dropdown_mun', 'value')]
#)

def build_chart(dropdown_mun):
     global fig, fig_geojson
     dff = df_desertion_dept[df_desertion_dept['name_dept'] == dropdown_mun]
     city_name = dff['code_dept'].unique()[0]
     MUN2_json['features'] = [city for city in MUN_json['features'] if city['properties']['DPTO_CCDGO'] == city_name]
#    #new center
     center_x=MUN2_json['features'][0]['geometry']['coordinates'][0][0][0]
     center_y=MUN2_json['features'][0]['geometry']['coordinates'][0][0][1]
     new_center=dict(lat=center_y, lon=center_x)
    
     fig_geojson = MUN2_json
     fig2 = px.choropleth_mapbox(dff,
                             geojson=MUN2_json,
                             locations='code_municip',
                             color=fig.color,
                             featureidkey="properties.MPIO_CCNCT",
                             zoom=6,
                             hover_name="name_municip",
                             mapbox_style="carto-positron",
                             center=new_center,
                             color_continuous_scale="blues",
                             )
     fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
     return fig2
    
def rebuild_chart(color_selected):
     global fig, fig_geojson
        
     #dff = fig.data_frame #df_desertion_dept[df_desertion_dept['name_dept'] == dropdown_mun]
     city_name = dff['code_dept'].unique()[0]
     #MUN2_json['features'] = [city for city in MUN_json['features'] if city['properties']['DPTO_CCDGO'] == city_name]
#     #new center
     #center_x=MUN2_json['features'][0]['geometry']['coordinates'][0][0][0]
     #center_y=MUN2_json['features'][0]['geometry']['coordinates'][0][0][1]
     #new_center=dict(lat=center_y, lon=center_x)
     fig3 = px.choropleth_mapbox(dff,
                             geojson=fig_geojson,
                             locations='code_municip',
                             color=color_selected,
                             featureidkey="properties.MPIO_CCNCT",
                             zoom=6,
                             hover_name="name_municip",
                             mapbox_style="carto-positron",
                             #center=fig.center,
                             color_continuous_scale="blues",
                             )
     fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
     return fig3    


##############################
#Map Layout
##############################
map=html.Div([
 #Place the main graph component here:
    sidebar_maps.sidebar,
    html.Div([dcc.Graph(figure=fig, id='maps_fig1')],style = MAP_BENCHMARK_STYLE),
    #dbc.Col(html.Div(dropdown.dropdown_mun)),
    html.Div(dropdown.dropdown_mun,style = RANKING_TABLE_BENCHMARK_STYLE)
   
], className="ds4a-body")



