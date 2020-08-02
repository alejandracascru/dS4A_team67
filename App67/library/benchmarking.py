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
from library.elements_all import sidebar_benchmarking

##############################
# Benchmarking
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
    "position": "absolute",
    "width": "35%",
    "left": "17rem",
    "top": "140px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.2 Ranking Table Styles
GROUP_TABLE_BENCHMARK_STYLE = {
    "position": "absolute",
    "width": "20%",
    "right": "1rem",
    "top": "140px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.3 Group Table Styles
RANKING_TABLE_BENCHMARK_STYLE = {
    "position": "absolute",
    "width": "20%",
    "right": "22%",
    "top": "140px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.4 Group Table Styles
SLACK_GRAPH_BENCHMARK_STYLE = {
    "position": "absolute",
    "width": "41%",
    "height": "200px",
    "right": "1rem",
    "top": "480px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.5 Efficiency Definition Styles
EFFICIENCY_DEF_STYLE ={
    "position": "absolute",
    "width": "35%",
    "height": "80px",
    "left": "17rem",
    "bottom": "10px",
    #"border": "1px solid #e7eff6",
    #"border-radius": "10px",
    'overflowY': 'scroll'
}

# ------------------------------
# 2. SQL Queries
# ------------------------------
# 2.1 Initial query
# ------------------------------
df_dropout_efficiency = def_data.runQuery("""
    select code_municip, name_municip as muni, benchmarking_rank  as rank, 
    benchmarking_efficiency as efficiency 
    from cluster_master_table_by_municipio cmtbm  ; """)
df_dropout_efficiency['efficiency'] = df_dropout_efficiency['efficiency'].astype(np.float64)
df_dropout_efficiency['efficiency_percent'] = df_dropout_efficiency['efficiency'].astype(float).map("{:.1%}".format)
df_dropout_efficiency.sort_values(by=['efficiency','muni'], ascending=[False,True], inplace=True)
# 2.1 Query function
# ------------------------------

# ------------------------------
# 3. Map
# ------------------------------
# 3.1 Loads JSON file
# ------------------------------
with open('data/MGN_MPIO_POLITICO_2.json') as geo:
    munijson = json.loads(geo.read())

# 3.2 Define initial map properties
# ------------------------------
EF_Map = px.choropleth_mapbox(df_dropout_efficiency,     # Data
        locations='code_municip',                # Column containing the identifiers used in the GeoJSON file
        featureidkey="properties.MPIO_CCNCT",    # Column in de JSON containing the identifier of the municipality.
        color='efficiency',                      # Column giving the color intensity of the region
        geojson=munijson,                        # The GeoJSON file
        zoom=4,                                  # Zoom
        mapbox_style="carto-positron",           # Mapbox style, for different maps you need a Mapbox account and a token
        center={"lat": 4.5709, "lon": -74.2973}, # Center
        color_continuous_scale="Viridis",        # Color Scheme
        opacity=0.8                              # Opacity of the map
        )
EF_Map.update_geos(fitbounds="locations", visible=False)
EF_Map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# ------------------------------
# 4. Ranking
# https://dash.plotly.com/datatable
# ------------------------------
ranking_table = dt.DataTable(
    id='benchmarking_rank_table',
    columns=[{"name": 'Rank', "id": 'rank'},
             {'name':'Municipality','id':'muni'},
             {'name':'Efficiency','id':'efficiency_percent'}],
    data=df_dropout_efficiency.to_dict('records'),
    style_table={'height': '280px', 'overflowY': 'auto'},
    style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
    style_cell_conditional=[
            {'if': {'column_id': 'rank'},'width': '15%'},#,'max-width': '15%'
            {'if': {'column_id': 'muni'},'width': '35%'},#,'max-width': '35%'
            {'if': {'column_id': 'efficiency_percent'},'width': '15%'}, #,'max-width': '15%'
        ],
    style_as_list_view=True,
    #style_data_conditional=[{
    #        'if': {'column_id': 'efficiency'},
    #        'format': FormatTemplate.percentage(1)
    #    }]
)

# ------------------------------
# 5. DMU Groups
# ------------------------------
refset_data = {'Reference Set': [['La Victoria', 'Tado'],
                  ['Tado','Bogota, D.C.','Sogamoso'],
                  ['Tado','Sogamoso'],
                  ['Bogota, D.C.','Sogamoso','Soledad'],
                  ['Sogamoso','Soledad'],
                  ['Bogota, D.C.','Soledad'],
                  ['La Victoria', 'Tado','Bogota, D.C.']],
        '# Municipalities': ['813 (75%)','121 (11%)','107 (10%)','22 (2%)','22 (2%)','22 (0%)','22 (0%)']}

refset_df = pd.DataFrame(refset_data, columns = ['Reference Set', '# Municipalities'])

group_table = dt.DataTable(
    id='benchmarking_group_table',
    columns=[{"name": i, "id": i} for i in refset_df.columns],
    data=refset_df.to_dict('records'),
    style_table={'height': '280px', 'overflowY': 'auto'},
    style_cell={
            'whiteSpace': 'normal',
            'height': 'auto'}
)

# ------------------------------
# 6. Slack/Waste
# ------------------------------
inputgraph_data = {'Label': ['# Students'],'% Slack': [0]}
bargraph_df = pd.DataFrame(inputgraph_data, columns = ['Label', '% Slack'])

slack_graph = px.bar(bargraph_df, x="Label", y="% Slack", height=200)
slack_graph.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# ------------------------------
# 7. Efficiency Definition
# ------------------------------
efficiency_def = html.Div([
        html.P('Efficient municipalities are those that produce the lesser school dropout while spending a given amount of the inputs:')]
)

# ------------------------------
# 8. Callback and DEA
# ------------------------------
@app.callback(
    [Output("benchmarking_map", "figure"),
     Output("benchmarking_rank_table","data"),
     Output("benchmarking_group_table","data"),
     Output("slack_graph", "figure")],
    [Input("DEA-button", "n_clicks")]
)
def on_button_click(n):
    if n is not None:
        # 1. Define set of input variables for DEA
        # 1.1 Get variable ids from checklist
        var_list = ''
        single_qote = "'"
        for var in sidebar_benchmarking.input_array:
            var_list = var_list + single_qote + var + single_qote + ','
        var_list = var_list[:-1]

        # 1.2 Get variable name from SQL table var_definition.
        df_var_name = def_data.runQuery(
            'select name, label from public.var_definition where var_id in (' + var_list + ');')

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
        if sidebar_benchmarking.area_array is not None:
            are_res = 'where region = ' + single_qote + sidebar_benchmarking.area_array + single_qote + ' '

        # 2.3 Define the SQL query
        benchmarking_sql_query = 'select code_municip, name_municip as muni, ' + var_col + \
            ' from cluster_master_table_by_municipio ' + \
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
            def_data.BCCO_DMU_PH2(df_benchmarking_data, dmu, -1 * ph1_dual.fun, inp, out)
            ph2 = linprog(c=def_data.obj2, A_eq=def_data.lhs_eq2, b_eq=def_data.rhs_eq2, bounds=def_data.bnd2, method="simplex")
            ef = ef.append({'dmu': dmu, 'efficiency': -1 / ph1_dual.fun,
                            'reference_set': def_data.BCCO_DMU_REFSET(df_benchmarking_data, inp, out, ph2.x),
                            'slack': def_data.BCCO_DMU_VAR(inp, out, ph1_dual.slack)}, ignore_index=True)

        # 5. Process the results
        # 5.1 Merge to get municipalities names
        ef = ef.merge(df_benchmarking_data[['DMU', 'muni']], left_on='dmu', right_on='DMU')
        ef = ef.sort_values(by=["efficiency", 'muni'], ascending=[False, True])
        ef["rank"] = ef["efficiency"].rank(ascending=False, method='min')
        ef['efficiency_percent'] = ef['efficiency'].astype(float).map("{:.1%}".format)
        ef['Municipality'] = ef['muni']

        # 5.2 Efficient Units and Reference set
        ef_dmu = ef[ef['efficiency']>=1][['dmu','muni']]
        ref_set = pd.DataFrame(ef[ef['efficiency'] < 1][['reference_set']].reset_index()['reference_set'].value_counts()).reset_index()

        def convert_dmu_to_string(array):
            new_array = []
            for dmu in array:
                if dmu in list(ef_dmu['dmu']):
                    new_array.append(ef_dmu[ef_dmu['dmu'] == dmu][['muni']].reset_index()['muni'][0])
            return new_array

        # From ref_set gets names and takeout non productive units
        refset_data = []
        for rs in ref_set['index']:
            line_set = []
            for dmu in rs:
                if dmu in list(ef_dmu['dmu']):
                    line_set.append(ef_dmu[ef_dmu['dmu'] == dmu][['muni']].reset_index()['muni'][0])
            refset_data.append(line_set)

        # This is the new Reference Set to print on screen.
        refset_df = pd.DataFrame({'Reference Set': refset_data,
                                  '# Municipalities': list(ref_set['reference_set'])},
                                 columns=['Reference Set', '# Municipalities'])

        new_group_data = refset_df.to_dict('records')

        # Refset for display in the map
        ef['Ref Municipality'] = ef['reference_set'].apply(convert_dmu_to_string)
        # 5.3 Slack Variables count
        slack = []
        for sl in ef['slack']:
            slack.extend(sl)
        slack_data = (pd.DataFrame(slack, columns=['Slack Count']))['Slack Count'].value_counts().reset_index()
        slack_data = slack_data.merge(df_var_name, left_on='index', right_on='name', how='left')
        slack_data = slack_data.rename(columns={'label': 'Feature'})

        new_slack_graph = px.bar(slack_data, x="Feature", y="Slack Count", height=200)
        new_slack_graph.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})


        # 6. Creates new map
        # 6.1 Loads JSON file
        # # ------------------------------
        map_url = ''
        if sidebar_benchmarking.area_array is None:
            map_url = 'data/municipios_1mn.json'
        elif sidebar_benchmarking.area_array == 'Amazonica':
            map_url = 'data/amazonica90.json'
        elif sidebar_benchmarking.area_array == 'Andina':
            map_url = 'data/andina90.json'
        elif sidebar_benchmarking.area_array == 'Caribe':
            map_url = 'data/caribe90.json'
        elif sidebar_benchmarking.area_array == 'Orinoquia':
            map_url = 'data/orinoquia90.json'
        elif sidebar_benchmarking.area_array == 'Pacifica':
            map_url = 'data/pacifico90.json'

        with open(map_url) as geo:
            munijson = json.loads(geo.read())

        # 6.2 Define new map properties
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
              opacity=0.5,                              # Opacity of the map
              hover_name='Municipality',
              hover_data=['Ref Municipality']
                                      )
        new_Map.update_geos(fitbounds="locations", visible=False)
        new_Map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        new_Rank_data = ef[['rank','muni','efficiency_percent']].to_dict('records')

    else:
        new_Map = EF_Map
        new_Rank_data = ranking_table.data
        new_group_data = group_table.data
        new_slack_graph = slack_graph

    return [new_Map,new_Rank_data,new_group_data,new_slack_graph]

# ------------------------------
# 9. Layout
# ------------------------------
benchmarking = html.Div([
    sidebar_benchmarking.sidebar,
    html.Div([dcc.Graph(figure=EF_Map, id='benchmarking_map')],style = MAP_BENCHMARK_STYLE),
    html.Div(efficiency_def,id='efficiency_def',style=EFFICIENCY_DEF_STYLE),
    html.Div([ranking_table],style = RANKING_TABLE_BENCHMARK_STYLE),
    html.Div([group_table],style = GROUP_TABLE_BENCHMARK_STYLE),
    html.Div([dcc.Graph(figure=slack_graph, id='slack_graph')],style = SLACK_GRAPH_BENCHMARK_STYLE)

], className="ds4a-body")

# TODO: add more functionality
# 1. Hover
# 1.1 Accordion, show variable description.
# 1.2 Map, show input and output values, efficiency, ranking, reference set, and cause of slack.
# 2. Click
# 2.1 Rank table, when click show map hover.
#
# TODO: fix initial efficiency data
# TODO: change query to cluster_table

