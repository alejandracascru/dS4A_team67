# Basics Requirements
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import numpy as np
from dash.dependencies import Input, Output, State

import json

# Recall app
from app import app
from library.elements_all import sidebar_maps
from library import def_data

##############################
# MAPS
##############################
# CONTENTS
# 1. Styles
# 2. SQL queries
# 3. Map
# 4. Ranking
# 5. DMU Groups
# 6. Slacks/Waste
# 7. Efficiency definition
# 8. Callback and DEA
# 9. Layout
# ------------------------------

# ------------------------------
# 1. Styles
# ------------------------------
# 1.1 Map Styles
MAP_MAPS_STYLE = {
     "position": "fixed",
     "width": "70%",
     "left": "17rem",
     "top": "140px",
     "border": "1px solid #e7eff6"
}

# ------------------------------
# 2. SQL Queries
# ------------------------------
# 2.1 Initial query
# ------------------------------
df_desertion = def_data.runQuery("""
    select code_dept, name_dept, avg(desertion_perc) as desertion_perc
    from master_table_by_municipio 
    where year_cohort = 2019
    group by code_dept, name_dept; """)
df_desertion['desertion_perc'] = df_desertion['desertion_perc'].astype(np.float64)
df_vars = def_data.runQuery("""select * from public.var_definition order by group_id;""")

# ------------------------------
# 3. MAP
# ------------------------------
# 3.1 Global variables
# ------------------------------
selected_var = 'desertion_perc'
selected_var_code = 3
selected_dpt = 'Antioquia'
label_fig = df_vars[df_vars['name'] == selected_var].reset_index()['label'][0]
# 3.2 Initial map
# ------------------------------
with open('data/MGN_MPIO_POLITICO.json') as geo:
     MUN_json = json.loads(geo.read())

with open('data/MGN_DPTO_POLITICO.json') as f:
     DEP_json = json.loads(f.read())
MUN2_json = DEP_json.copy()

map_fig = px.choropleth_mapbox(df_desertion,
            geojson=DEP_json,
            color="desertion_perc",
            locations="code_dept",
            featureidkey="properties.DPTO_CCDGO",
            color_continuous_scale = "Blues",
            center={"lat": 4.94, "lon": -73.77},
            hover_name="name_dept",
            mapbox_style="carto-positron", zoom=4)
map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                       coloraxis_colorbar=dict(
                       title=label_fig))

# 3.2 Update map
# ------------------------------
input_array_map = np.append([Input('maps_dropdown_depto', 'value')],
                            [Input(f'mapLabel-{i}', 'n_clicks') for i in sidebar_maps.df_vars['var_id']])
@app.callback(Output('maps_fig1', 'figure'),list(input_array_map))
def build_chart(depto_val,*args):
    # 3.2.1 Determine is a variable is selected and which
    # ------------------------------
    global selected_var_code
    df_vars = sidebar_maps.df_vars.copy()
    changed_label_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    for i in df_vars['var_id']:
        if 'mapLabel-' + i in changed_label_id:
            selected_var_code = i
    selected_var = df_vars.loc[df_vars['var_id'] == str(selected_var_code)]['name'].reset_index()['name'][0]

    single_qote = "'"

    if False: # If no change in either the dropdown or the labels, then do nothing.
        return map_fig
    else:
        # 3.2.2 Map by department (drop down mun is None)
        if depto_val is None:
            # 3.2.2.1 Query desired variable
            # ------------------------------
            selected_var="desertion_perc"
            sql_query = 'select code_dept, name_dept, avg(' + selected_var + ') as ' + selected_var + ' ' + \
                'from master_table_by_municipio ' + \
                'where year_cohort = 2019 ' + \
                'group by code_dept, name_dept;'
            df_var_all_dpto = def_data.runQuery(sql_query)
            df_var_all_dpto[selected_var] = df_var_all_dpto[selected_var].astype(np.float64)
            label_fig = df_vars[df_vars['name'] == selected_var].reset_index()['label'][0]
            label_tittle =  df_vars[df_vars['name'] == selected_var].reset_index()['description'][0]
            # 3.2.2.2 Define new map
            # ------------------------------
            new_map = px.choropleth_mapbox(df_var_all_dpto,
               geojson=DEP_json,
               color=selected_var,
               locations="code_dept",
               featureidkey="properties.DPTO_CCDGO",
               color_continuous_scale="Blues",
               center={"lat": 4.94, "lon": -73.77},
               hover_name="name_dept",
               mapbox_style="carto-positron", zoom=4)
            
            new_map.update_layout(margin={"r":0,"l":0,"b":0},
                                  title_text=label_tittle,
                                  coloraxis_colorbar=dict(
                                  title=label_fig))
            return new_map
        # 3.2.3 Map by municipality (drop down mun is not None)
        else:
            # 3.2.3.1 Query desired variable
            # ------------------------------
            sql_query = 'select code_municip, code_dept, name_municip, dane_alu_18_p, dane_tic_03_1_p, ' + \
                        'po_pob_rural_10mil, dane_alu_12_p, dane_tic_01, ' + selected_var + ' ' + \
                        'from master_table_by_municipio ' + \
                        'where year_cohort = 2019 ' \
                        'and code_dept = ' + single_qote + depto_val + single_qote + ';'

            df_var_by_dpto = def_data.runQuery(sql_query)
            df_var_by_dpto[selected_var] = df_var_by_dpto[selected_var].astype(np.float64)
            
            
            # 3.2.3.2 Filtering the Departament
            # ------------------------------
            MUN2_json['features'] = [city for city in MUN_json['features'] if city['properties']['DPTO_CCDGO'] == depto_val]
            center_x=MUN2_json['features'][0]['geometry']['coordinates'][0][0][0]
            center_y=MUN2_json['features'][0]['geometry']['coordinates'][0][0][1]
            new_center=dict(lat=center_y, lon=center_x)
            
            
            # 3.2.3.3 MAp Layout
            # ------------------------------
            label_fig = df_vars[df_vars['name'] == selected_var].reset_index()['label'][0]
            label_tittle =  df_vars[df_vars['name'] == selected_var].reset_index()['description'][0]
            df_var_by_dpto = df_var_by_dpto.rename({'dane_alu_18_p': '% Students afternoon',
                                                    'dane_tic_01': 'Avg computers x100 stu.',
                                                    'dane_alu_12_p': '% Transferred students',
                                                    'dane_tic_03_1_p': '% Schools with electricity',
                                                    'po_pob_rural_10mil': '% Habitants (towns-rural)'}, axis=1) 
            
            # 3.2.3.4 Define new map
            # ------------------------------
            new_map = px.choropleth_mapbox(df_var_by_dpto,
                     geojson=MUN2_json,
                     locations='code_municip',
                     color=selected_var,
                     featureidkey="properties.MPIO_CCNCT",
                     hover_name="name_municip",
                     mapbox_style="carto-positron",
                     center=new_center,
                     hover_data=['% Students afternoon','% Habitants (towns-rural)', 'Avg computers x100 stu.',
                                 '% Schools with electricity',
                                 '% Transferred students'],
                     zoom=6,
                     color_continuous_scale="blues",
                     )
            new_map.update_layout(margin={"r":0,"l":0,"b":0},
                                  title_text=label_tittle,
                                  coloraxis_colorbar=dict(
                                  title=label_fig))
            return new_map

    



##############################
#Map Layout
##############################
map = html.Div([
    sidebar_maps.sidebar,
    html.Div([dcc.Graph(figure=map_fig, id='maps_fig1')],style = MAP_MAPS_STYLE)
    #dbc.Col(html.Div(dropdown.dropdown_mun)),
    #html.Div(dropdown.dropdown_mun)
   
], className="ds4a-body")



