import json
import numpy as np
import plotly.express as px
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html

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
# 7. Layout
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
# ------------------------------
ranking_table = dt.DataTable(
    id='table',
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

# ------------------------------
# 7. Layout
# ------------------------------
benchmarking = html.Div([
    sidebar.sidebar,
    html.Div([dcc.Graph(figure=EF_Map, id='US_map')],style = MAP_BENCHMARK_STYLE),
    html.Div([ranking_table],style = RANKING_TABLE_BENCHMARK_STYLE),
    html.Div([group_table],style = GROUP_TABLE_BENCHMARK_STYLE),
    html.Div([dcc.Graph(figure=slack_graph, id='slack_graph')],style = SLACK_GRAPH_BENCHMARK_STYLE)

], className="ds4a-body")