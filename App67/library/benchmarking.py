import json
import plotly.express as px
import dash_html_components as html

from library import def_data
from library.elements_all import sidebar

##############################
# Benchmarking Layout
##############################
# CONTENTS
# 1. Styles
# 3. SQL queries
# 4. Map
# 5. Ranking
# 6. DMU Groups
# 7. Inp. Variables
# ------------------------------


# ------------------------------
# 2. SQL Queries
# ------------------------------
# 2.1 Query variables
#df_dropout_efficiency = def_data.runQuery("""select code_municip, mtbm.name_municip as muni, mtbm.dane_alu_01 as alumns, (mtbm.dane_alu_01 - mtbm.dane_alu_11) as nodropouts
#    from master_table_by_municipio mtbm
#    where mtbm.year_cohort = 2019
#    and region = 'Caribe'
#    and mtbm.dane_alu_01 is not null
#    and mtbm.dane_alu_11 is not null
#    and mtbm.dane_alu_01 > 0;
#    ;""")
# ------------------------------
# 3. Map
# ------------------------------
#with open('/Users/alberto/Documents/GitHub/dS4A_team67/App67/data/MGN_MPIO_POLITICO.json') as geo:
#    munijson = json.loads(geo.read())
#EF_Map = px.choropleth_mapbox(df_dropout_efficiency,                         #Data
#        locations='code_municip',                   #Column containing the identifiers used in the GeoJSON file
#        featureidkey="properties.MPIO_CCNCT",
#        color='nodropouts',                         #Column giving the color intensity of the region
#        geojson=munijson,                           #The GeoJSON file
#        zoom=4,                                     #Zoom
#        mapbox_style="carto-positron",              #Mapbox style, for different maps you need a Mapbox account and a token
#        center={"lat": 4.0902, "lon": -75.7129},    #Center
#        color_continuous_scale="Viridis",           #Color Scheme
#        opacity=0.5                                 #Opacity of the map
#        )

benchmarking = html.Div([
    sidebar.sidebar
], className="ds4a-body")