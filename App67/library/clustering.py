# Basics Requirements
import dash_html_components as html
import dash_core_components as dcc
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import numpy as np
import json
import dash
import dash_table
import pandas as pd
# Recall app
from app import app
from library.elements_all import sidebar_benchmarking
from library.elements_all import dropdown
from library import def_data


##############################
# Clustering
##############################
# CONTENTS
#  1. Styles
#  2. SQL queries
#  3. Map
#  4. Figure 3D
#  5. First text
#  6. Histogram
#  7. Features table
#  8. Drop down for different clusters
#  9. Scatterplot
# 10. Boxplot
# 11. Second text
# 12. Layout
# ------------------------------

# ------------------------------
# 1. Styles
# ------------------------------
# 1.1 Map Styles
STYLE_CLUSTER_MAP = {
    "position": "absolute",
    "width": "47%",
    "height": "400px",
    "left": "2%",
    "top": "240px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}
# 1.2 Map Styles
STYLE_CLUSTER_FIGURE3D = {
    "position": "absolute",
    "width": "47%",
    "height": "400px",
    "right": "2%",
    "top": "240px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.3 First Text
STYLE_CLUSTER_FIRST_TEXT = {
    "position": "absolute",
    "width": "94%",
    "height": "100px",
    "left": "3%",
    "right": "3%",
    "top": "140px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.4 Histogram
STYLE_CLUSTER_HISTOGRAM = {
    "position": "absolute",
    "width": "47%",
    "height": "450px",
    "left": "2%",
    "top": "660px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px",
    'overflowY': 'scroll'
}

# 1.5 Features
STYLE_CLUSTER_FEATURES = {
    "position": "absolute",
    "width": "20%",
    "height": "450px",
    "right": "1rem",
    "top": "660px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.6 Dropdown
STYLE_CLUSTER_DROPDOWN = {
    "position": "absolute",
    "width": "90%",
    "height": "50px",
    "right": "1rem",
    "top": "1110px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.7 Scatterplot
STYLE_CLUSTER_SCATTERPLOT = {
    "position": "absolute",
    "width": "20%",
    "height": "450px",
    "right": "1rem",
    "top": "1170px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.8 Boxplot
STYLE_CLUSTER_BOXPLOT= {
    "position": "absolute",
    "width": "20%",
    "height": "450px",
    "right": "1rem",
    "top": "1170px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.9 Second text
STYLE_CLUSTER_SECOND_TEXT = {
"position": "absolute",
    "width": "20%",
    "height": "80px",
    "right": "1rem",
    "top": "1640px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}
# ------------------------------
# 2. SQL Queries
# ------------------------------
# 2.1 Initial query
# ------------------------------
# 2.1 Initial query
# ------------------------------
df_clusters = def_data.runQuery("""
    select 1 as Rank, code_municip, name_municip as muni, dane_alu_01 as efficiency,
    dane_alu_02, dane_doc_01 
    from master_table_by_municipio 
    where year_cohort = 2019 
    and dane_alu_01 is not null  and dane_alu_11 is not null  
    and dane_alu_01 > 0; """)
df_clusters['efficiency'] = df_clusters['efficiency'].astype(np.float64)

df_vars = def_data.runQuery("""
    SELECT column_name as feature 
    FROM information_schema.columns
    WHERE table_schema = 'public'
    AND table_name   = 'master_table_by_municipio'
    LIMIT 118; """)

# ------------------------------
#  3. Map
# ------------------------------
# ------------------------------
# 3.1 Loads JSON file
# ------------------------------
with open('data/municipios95.json') as geo:
    munijson = json.loads(geo.read())

# 3.2 Define initial map properties
# ------------------------------
df_clusters['cluster'] = [str(np.random.randint(1, 5)) for i in range(df_clusters['efficiency'].shape[0])]
cl_map = px.choropleth_mapbox(df_clusters,     # Data
        locations='code_municip',                # Column containing the identifiers used in the GeoJSON file
        featureidkey="properties.MPIO_CCNCT",    # Column in de JSON containing the identifier of the municipality.
        color='cluster',                         # Column giving the color intensity of the region
        geojson=munijson,                        # The GeoJSON file
        zoom=4,                                  # Zoom
        mapbox_style="white-bg",           # Mapbox style, for different maps you need a Mapbox account and a token
        center={"lat": 4.5709, "lon": -74.2973}, # Center
        color_continuous_scale="Viridis",        # Color Scheme
        opacity=0.5,                             # Opacity of the map
        height=380,
        hover_name='muni',
        hover_data=['cluster','efficiency']
        )
cl_map.update_geos(fitbounds="locations", visible=False)
cl_map.update_layout(title_text ='Municipalities by cluster',margin={"r":20,"t":40,"l":20,"b":0})

cluster_map = html.Div([dcc.Graph(figure=cl_map, id='cluster_map')],style=STYLE_CLUSTER_MAP)
# ------------------------------
#  4. Figure 3D
# ------------------------------
cl_scatter = px.scatter_3d(df_clusters, x="dane_doc_01", y="dane_alu_02", z="cluster",
                           color="dane_doc_01",hover_name="muni",
                           opacity=0.5)
cluster_figure_3D = html.Div([dcc.Graph(figure=cl_scatter, id='cluster_map')],style=STYLE_CLUSTER_FIGURE3D)
# ------------------------------
#  5. First text
# ------------------------------
cluster_first_text = html.Div(html.P('First text -> Resultado del test Kruskal'),style=STYLE_CLUSTER_FIRST_TEXT)
# ------------------------------
#  6. Histogram
# ------------------------------
df_vars['weight'] = [np.random.randint(1, 100) for i in range(df_vars['feature'].shape[0])]
#ax = sns.barplot(x="feature", y="weight", data=df_vars,palette="PuBu_r")
df_vars = df_vars.sort_values(by='weight', ascending=False)
fig = px.bar(df_vars, x="weight", y="feature", orientation='h', height=2000)
cluster_histogram = html.Div([dcc.Graph(figure=fig, id='cluster_hist')],style=STYLE_CLUSTER_HISTOGRAM)
# ------------------------------
#  7. Features table
# ------------------------------
cluster_features = html.Div(html.P('Features selection'),style=STYLE_CLUSTER_FEATURES)
# ------------------------------
#  8. Drop down for different clusters
# ------------------------------
cluster_dropdown = html.Div(html.P('Dropdown'),style=STYLE_CLUSTER_DROPDOWN)
# ------------------------------
#  9. Scatterplot
# ------------------------------
cluster_scatterplot = html.Div(html.P('Scatterplot'),style=STYLE_CLUSTER_SCATTERPLOT)
# ------------------------------
# 10. Boxplot
# ------------------------------
cluster_boxplot = html.Div(html.P('Boxplot'),style=STYLE_CLUSTER_BOXPLOT)
# ------------------------------
# 11. Second text
# ------------------------------
cluster_second_text = html.Div(html.P('Second Text'),style=STYLE_CLUSTER_SECOND_TEXT)
# ------------------------------
# 12. Layout
# ------------------------------
clustering = html.Div([
    cluster_map,
    cluster_figure_3D,
    cluster_first_text,
    cluster_histogram,
    cluster_features,
    cluster_dropdown,
    cluster_scatterplot,
    cluster_boxplot,
    cluster_second_text
], className="ds4a-body")


