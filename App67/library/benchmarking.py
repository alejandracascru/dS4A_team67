import json
import pandas as pd
import numpy as np
from decimal import *
import plotly.express as px
from scipy.optimize import linprog
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# Recall app
from app import app
from library import def_data
from library.elements_all import sidebar

##############################
# Benchmarking Layout
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
MAP_BENCHMARK_STYLE = {
    "position": "fixed",
    "width": "35%",
    "left": "17rem",
    "top": "140px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.2 Ranking Table Styles
RANKING_TABLE_BENCHMARK_STYLE = {
    "position": "fixed",
    "width": "20%",
    "right": "1rem",
    "top": "140px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.3 Group Table Styles
GROUP_TABLE_BENCHMARK_STYLE = {
    "position": "fixed",
    "width": "20%",
    "right": "22%",
    "top": "140px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.4 Group Table Styles
SLACK_GRAPH_BENCHMARK_STYLE = {
    "position": "fixed",
    "width": "41%",
    "height": "200px",
    "right": "1rem",
    "top": "480px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# ------------------------------
# 2. SQL Queries
# ------------------------------
# 2.1 Initial query
# ------------------------------
df_dropout_efficiency = def_data.runQuery("""
    select code_municip, mtbm.dane_alu_11 as nodropouts
    from master_table_by_municipio mtbm 
    where mtbm.year_cohort = 2019 
    and mtbm.dane_alu_01 is not null 
    and mtbm.dane_alu_11 is not null
    and mtbm.dane_alu_01 > 0;""")
df_dropout_efficiency['nodropouts'] = df_dropout_efficiency['nodropouts'].astype(np.float64)
# 2.1 Query function
# ------------------------------

# ------------------------------
# 3. Map
# ------------------------------
# 3.1 Loads JSON file
# ------------------------------
with open('data/municipios95.json') as geo:
    munijson = json.loads(geo.read())

# 3.2 Define initial map properties
# ------------------------------
EF_Map = px.choropleth_mapbox(df_dropout_efficiency,     # Data
        locations='code_municip',                # Column containing the identifiers used in the GeoJSON file
        featureidkey="properties.MPIO_CCNCT",    # Column in de JSON containing the identifier of the municipality.
        color='nodropouts',                      # Column giving the color intensity of the region
        geojson=munijson,                        # The GeoJSON file
        zoom=4,                                  # Zoom
        mapbox_style="white-bg",           # Mapbox style, for different maps you need a Mapbox account and a token
        center={"lat": 4.5709, "lon": -74.2973}, # Center
        color_continuous_scale="Viridis",        # Color Scheme
        opacity=0.5                              # Opacity of the map
        )
EF_Map.update_geos(fitbounds="locations", visible=False)
EF_Map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# ------------------------------
# 4. Ranking
# https://dash.plotly.com/datatable
# ------------------------------
ranking_table = dt.DataTable(
    id='benchmarking_rank_table',
    columns=[{"name": i, "id": i} for i in df_dropout_efficiency.columns],
    data=df_dropout_efficiency.to_dict('records'),
    style_table={'height': '280px', 'overflowY': 'auto'}
)

# ------------------------------
# 5. DMU Groups
# ------------------------------
group_table = dt.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df_dropout_efficiency.columns],
    data=df_dropout_efficiency.to_dict('records'),
    style_table={'height': '280px', 'overflowY': 'auto'}
)

# ------------------------------
# 6. Slack/Waste
# ------------------------------

slack_graph = px.histogram(df_dropout_efficiency, x="nodropouts", height=200)
slack_graph.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# ------------------------------
# 8. Callback and DEA
# ------------------------------
@app.callback(
    [Output("benchmarking_map", "figure"),Output("benchmarking_rank_table","data")], [Input("DEA-button", "n_clicks")]
)
def on_button_click(n):
    if n is not None:
        # 1. Define set of input variables for DEA
        # 1.1 Get variable ids from checklist
        var_list = ''
        single_qote = "'"
        for var in sidebar.input_array:
            var_list = var_list + single_qote + var + single_qote + ','
        var_list = var_list[:-1]

        # 1.2 Get variable name from SQL table var_definition.
        df_var_name = def_data.runQuery(
            'select name from public.var_definition where var_id in (' + var_list + ');')

        # 2. Define the SQL query.
        benchmarking_sql_query = ''            # SQL query.
        var_col = ''                    # Columns for query.
        var_res = ''                    # Restrictions for query.
        are_res = ''                    # Restriction for the area.

        # 2.1 Define columns and restrictions for the query
        for var in df_var_name['name']:
            var_col = var_col + var + ','
            var_res = var_res + ' and ' + var + ' is not null '
        var_col = var_col + '(dane_alu_01 - dane_alu_11) as nodropouts'
        var_res = var_res + ' and dane_alu_01 > 0; '

        # 2.2 Define the region restriction
        if sidebar.area_array is not None:
            are_res = 'and region = ' + single_qote + sidebar.area_array + single_qote + ' '

        # 2.3 Define the SQL query
        benchmarking_sql_query = 'select code_municip, name_municip as muni, ' + var_col + \
            ' from master_table_by_municipio where year_cohort = 2019 ' + \
            are_res + var_res

        # 3. Get data from SQL table master_table_by_municipio.
        df_benchmarking_data = def_data.runQuery(benchmarking_sql_query)

        # 4. Performs DEA calculations
        df_benchmarking_data = df_benchmarking_data.rename(columns={'code_municip': 'DMU'})

        # 4.1 Define the input and output variables
        inp = df_var_name['name'].tolist()
        out = ['nodropouts']

        # 4.2 Load the models for Phase I and Phase II
        def_data.BCCO_Base_PH1(df_benchmarking_data, inp, out)
        def_data.BCCO_Base_PH2(df_benchmarking_data, inp, out)

        # 4.3 Creates data frame for resulting efficiencies
        ef = pd.DataFrame(columns=['dmu', 'efficiency', 'reference_set', 'slack'])

        # 4.4 Recover global variables


        # 4.5 Solves for all DMUs
        for dmu in df_benchmarking_data['DMU'].tolist():
            def_data.BCCO_DMU_PH1(df_benchmarking_data, dmu, inp, out)
            ph1_dual = linprog(c=def_data.obj1, A_ub=def_data.lhs_ineq1, b_ub=def_data.rhs_ineq1, A_eq=def_data.lhs_eq1, b_eq=def_data.rhs_eq1, bounds=def_data.bnd1, method="simplex")
            def_data.BCCO_DMU_PH2(df_benchmarking_data, dmu, -1 * Decimal(ph1_dual.fun), inp, out)
            ph2 = linprog(c=def_data.obj2, A_eq=def_data.lhs_eq2, b_eq=def_data.rhs_eq2, bounds=def_data.bnd2, method="simplex")
            ef = ef.append({'dmu': dmu, 'efficiency': -1 / ph1_dual.fun,
                            'reference_set': def_data.BCCO_DMU_REFSET(df_benchmarking_data, inp, out, ph2.x),
                            'slack': def_data.BCCO_DMU_VAR(inp, out, ph1_dual.slack)}, ignore_index=True)

        # 5. Creates new map
        # 5.1 Loads JSON file
        # # ------------------------------
        map_url = ''
        if sidebar.area_array is None:
            map_url = 'data/municipios95.json'
        elif sidebar.area_array == 'Amazonica':
            map_url = 'data/amazonica90.json'
        elif sidebar.area_array == 'Andina':
            map_url = 'data/andina90.json'
        elif sidebar.area_array == 'Caribe':
            map_url = 'data/caribe90.json'
        elif sidebar.area_array == 'Orinoquia':
            map_url = 'data/orinoquia90.json'
        elif sidebar.area_array == 'Pacifica':
            map_url = 'data/pacifico90.json'

        with open(map_url) as geo:
            munijson = json.loads(geo.read())

        # 5.2 Define new map properties
        # ------------------------------
        new_Map = px.choropleth_mapbox(ef,               # Data
              locations='dmu',                          # Column containing the identifiers used in the GeoJSON file
              featureidkey="properties.MPIO_CCNCT",     # Column in de JSON containing the identifier of the municipality.
              color='efficiency',                       # Column giving the color intensity of the region
              geojson=munijson,                         # The GeoJSON file
              zoom=4,                                   # Zoom
              mapbox_style="white-bg",                  # Mapbox style, for different maps you need a Mapbox account and a token
              center={"lat": 4.5709, "lon": -74.2973},  # Center
              color_continuous_scale="Viridis",         # Color Scheme
              opacity=0.5                               # Opacity of the map
                                      )
        new_Map.update_geos(fitbounds="locations", visible=False)
        new_Map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        new_Rank_data = ef[['dmu','efficiency']].to_dict('records')

    else:
        new_Map = EF_Map
        new_Rank_data = group_table.data

    return [new_Map,new_Rank_data]

# ------------------------------
# 9. Layout
# ------------------------------
benchmarking = html.Div([
    sidebar.sidebar,
    html.Div([dcc.Graph(figure=EF_Map, id='benchmarking_map')],style = MAP_BENCHMARK_STYLE),
    html.Div([ranking_table],style = RANKING_TABLE_BENCHMARK_STYLE),
    html.Div([group_table],style = GROUP_TABLE_BENCHMARK_STYLE),
    html.Div([dcc.Graph(figure=slack_graph, id='slack_graph')],style = SLACK_GRAPH_BENCHMARK_STYLE)

], className="ds4a-body")