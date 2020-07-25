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
     "width": "50%",
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


# ------------------------------
# 3. MAP
# ------------------------------
# 3.1 Global variables
# ------------------------------
selected_var = 'desertion_perc'
selected_var_code = 3
selected_dpt = 'Antioquia'
# 3.2 Initial map
# ------------------------------
with open('data/MGN_MPIO_POLITICO.json') as geo:
     MUN_json = json.loads(geo.read())

with open('data/MGN_DPTO_POLITICO.json') as f:
     DEP_json = json.loads(f.read())

map_fig = px.choropleth_mapbox(df_desertion,
            geojson=DEP_json,
            color="desertion_perc",
            locations="code_dept",
            featureidkey="properties.DPTO_CCDGO",
            color_continuous_scale = "Blues",
            center={"lat": 4.94, "lon": -73.77},
            hover_name="name_dept",
            mapbox_style="carto-positron", zoom=4)
map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

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
            sql_query = 'select code_dept, name_dept, avg(' + selected_var + ') as ' + selected_var + ' ' + \
                'from master_table_by_municipio ' + \
                'where year_cohort = 2019 ' + \
                'group by code_dept, name_dept;'
            df_var_all_dpto = def_data.runQuery(sql_query)
            df_var_all_dpto[selected_var] = df_var_all_dpto[selected_var].astype(np.float64)
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
            new_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            return new_map
        # 3.2.3 Map by municipality (drop down mun is not None)
        else:
            # 3.2.3.1 Query desired variable
            # ------------------------------
            sql_query = 'select code_municip, code_dept, name_municip, ' + selected_var + ' ' + \
                        'from master_table_by_municipio ' + \
                        'where year_cohort = 2019 ' \
                        'and code_dept = ' + single_qote + depto_val + single_qote + ';'

            df_var_by_dpto = def_data.runQuery(sql_query)
            df_var_by_dpto[selected_var] = df_var_by_dpto[selected_var].astype(np.float64)

            # 3.2.3.2 Define new map
            # ------------------------------
            #city_name = df_var_by_dpto['code_dept'].unique().reset_index()['code_dept'][0]
            new_map = px.choropleth_mapbox(df_var_by_dpto,
                     geojson=MUN_json,
                     locations='code_municip',
                     color=selected_var,
                     featureidkey="properties.MPIO_CCNCT",
                     zoom=5,
                     hover_name="name_municip",
                     mapbox_style="carto-positron",
                     center={"lat": 4.94, "lon": -73.77},
                     color_continuous_scale="blues",
                     )
            new_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
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



