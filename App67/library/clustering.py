# Basics Requirements
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import numpy as np
import json

# Recall app
from app import app
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
# 12. Empty space
# 13. Callback
# 14. Layout
# ------------------------------

# ------------------------------
# 1. Styles
# ------------------------------
# 1.1 Map Styles
STYLE_CLUSTER_MAP = {
    "position": "absolute",
    "width": "42%",
    "height": "420px",
    "left": "7%",
    "top": "140px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}
# 1.2 Map Styles
STYLE_CLUSTER_FIGURE3D = {
    "position": "absolute",
    "width": "42%",
    "height": "400px",
    "right": "7%",
    "top": "240px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.3 First Text
STYLE_CLUSTER_FIRST_TEXT = {
    "position": "absolute",
    "width": "42%",
    "height": "90px",
    "right": "7%",
    "top": "140px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.4 Histogram
STYLE_CLUSTER_HISTOGRAM = {
    "position": "absolute",
    "width": "42%",
    "height": "500px",
    "left": "7%",
    "top": "570px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px",
    'overflowY': 'scroll'
}

# 1.5 Features
STYLE_CLUSTER_FEATURES = {
    "position": "absolute",
    "width": "42%",
    "height": "420px",
    "right": "7%",
    "top": "650px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.6 Dropdown
STYLE_CLUSTER_DROPDOWN = {
    "position": "absolute",
    "width": "42%",
    "height": "60px",
    "left": "7%",
    "top": "1080px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.7 Scatterplot
STYLE_CLUSTER_SCATTERPLOT = {
    "position": "absolute",
    "width": "42%",
    "height": "450px",
    "left": "7%",
    "top": "1150px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.8 Boxplot
STYLE_CLUSTER_BOXPLOT= {
    "position": "absolute",
    "width": "42%",
    "height": "350px",
    "right": "7%",
    "top": "1080px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.9 Second text
STYLE_CLUSTER_SECOND_TEXT = {
"position": "absolute",
    "width": "42%",
    "height": "160px",
    "right": "7%",
    "top": "1440px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.10 Second text
STYLE_CLUSTER_END_SPACE = {
"position": "absolute",
    "width": "42%",
    "height": "20px",
    "right": "7%",
    "top": "1600px"
}
# ------------------------------
# 2. SQL Queries
# ------------------------------
# 2.1 Query for cluster by municipality
# ------------------------------
df_clusters = def_data.runQuery("""
    select code_municip, name_municip, desertion_no, me_cobertura_neta, desertion_perc, deser_perc_rank, 
    cobertura_rank, desercion_rank, dane_doc_31
    from cluster_master_table_by_municipio; """)
for col in ['desertion_no', 'me_cobertura_neta', 'desertion_perc','dane_doc_31']:
        df_clusters[col] = df_clusters[col].astype(np.float64)
df_clusters.rename(columns = {
    "name_municip": "Municipio", "desertion_no": "# Dropouts",
    "me_cobertura_neta": "Coverage", "desertion_perc": "% Dropouts",
    "deser_perc_rank": "Cluster Description","cobertura_rank": "Coverage Type",
    "desercion_rank": "Desertion Type"}, inplace = True)
df_clusters['Cluster'] = df_clusters['Cluster Description'].astype(str).str[0]
# 2.2 Query for features
# ------------------------------
df_vars = def_data.runQuery("""
    select cvr.var_id, cvr.var_name, vd.label, vd.description, cvr.weight  
    from cluster_vars_ranking cvr 
    left join var_definition vd 
    on cvr.var_id  = vd.var_id ; """)
df_vars['weight'] = df_vars['weight'].astype(np.float64)
df_vars.rename(columns = {"weight": "Weight",'label':'Feature'}, inplace = True)
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
cl_map = px.choropleth_mapbox(df_clusters,     # Data
        locations='code_municip',                # Column containing the identifiers used in the GeoJSON file
        featureidkey="properties.MPIO_CCNCT",    # Column in de JSON containing the identifier of the municipality.
        color='Cluster',                         # Column giving the color intensity of the region
        geojson=munijson,                        # The GeoJSON file
        zoom=4,                                  # Zoom
        mapbox_style="white-bg",           # Mapbox style, for different maps you need a Mapbox account and a token
        center={"lat": 4.5709, "lon": -74.2973}, # Center
        color_continuous_scale="Viridis",        # Color Scheme
        opacity=0.5,                             # Opacity of the map
        height=380,
        hover_name='Municipio',
        hover_data=['# Dropouts','Coverage','% Dropouts']
        )
cl_map.update_geos(fitbounds="locations", visible=False)
cl_map.update_layout(title_text ='Municipalities by cluster',margin={"r":20,"t":40,"l":20,"b":0})

cluster_map = html.Div([dcc.Graph(figure=cl_map, id='cluster_map')],style=STYLE_CLUSTER_MAP)
# ------------------------------
#  4. Figure 3D
# ------------------------------
cl_scatter = px.scatter_3d(df_clusters, x="# Dropouts", y="Coverage", z="% Dropouts",
                           color="Cluster",hover_name="Municipio",
                           opacity=0.5)
cluster_figure_3D = html.Div([dcc.Graph(figure=cl_scatter, id='cluster_map')],style=STYLE_CLUSTER_FIGURE3D)
# ------------------------------
#  5. First text
# ------------------------------
cluster_first_text = html.Div(html.P('First text -> Resultado del test Kruskal'),style=STYLE_CLUSTER_FIRST_TEXT)
# ------------------------------
#  6. Histogram
# ------------------------------
df_vars = df_vars.sort_values(by='Weight', ascending=True)
cluster_hist = px.bar(df_vars, x="Weight", y="Feature", hover_data=['description'],
              title="Feature Weights", orientation='h', height=2000)
cluster_histogram = html.Div([dcc.Graph(figure=cluster_hist, id='cluster_hist')],style=STYLE_CLUSTER_HISTOGRAM)
# ------------------------------
#  7. Features table
# ------------------------------
cluster_features = html.Div(html.P('Features selection'),style=STYLE_CLUSTER_FEATURES)
# ------------------------------
#  8. Drop down for different clusters
# ------------------------------
cluster_var_drop = html.Div([
    dcc.Dropdown(
    id='cluster_var_drop',
    options=[{'label':df_vars['Feature'][i],'value':df_vars['var_id'][i]} for i in range(df_vars.shape[0])],
    value=280
    )
])

cluster_radio_log = dcc.RadioItems(
    options=[
        {'label': '   Linear   ', 'value': 'linear'},
        {'label': '   Log(x)   ', 'value': 'log'}
    ],
    value='linear',
    labelStyle={'display': 'inline-block'},
    id = 'cluster_radio_log'
)

cluster_dropdown = html.Div([cluster_var_drop,cluster_radio_log,html.P('Scatterplot')],style=STYLE_CLUSTER_DROPDOWN)
# ------------------------------
#  9. Scatterplot
# ------------------------------
cluster_select_drop = html.Div([
    dcc.Dropdown(
    id='cluster_select_drop',
    options=[
        {'label': 'Cluster 1: Low Dropput, Low Coverage', 'value': '1_DS_Baja-CB_Baja'},
        {'label': 'Cluster 2: Low Dropput, High Coverage', 'value': '2_DS_Baja-CB_Alta'},
        {'label': 'Cluster 3: High Dropput, Low Coverage', 'value': '3_DS_Alta-CB_Baja'},
        {'label': 'Cluster 4: High Dropput, High Coverage', 'value': '4_DS_Alta-CB_Alta'}
    ])
])

cluster_radio_y = dcc.RadioItems(
    id='cluster_radio_y',
    options=[
        {'label': 'Coverage', 'value': 'Coverage'},
        {'label': '# Dropouts', 'value': '# Dropouts'},
        {'label': '% Dropouts', 'value': '% Dropouts'}
    ],
    value='% Dropouts',
    labelStyle={'display': 'inline-block'}
)

cluster_scatter = px.scatter(df_clusters, x='dane_doc_31', y='% Dropouts')

cluster_scatterplot = html.Div([cluster_select_drop,
                                cluster_radio_y,
                                dcc.Graph(figure=cluster_scatter, id='cluster_scatter')],
                               style=STYLE_CLUSTER_SCATTERPLOT)
# ------------------------------
# 10. Boxplot
# ------------------------------
cluster_box = px.box(df_clusters, x="Coverage Type", y="dane_doc_31", color="Desertion Type",
             points="all", title="Box plot of blabla", hover_data=["Municipio"])
cluster_boxplot = html.Div([dcc.Graph(figure=cluster_box, id='cluster_box')],style=STYLE_CLUSTER_BOXPLOT)
# ------------------------------
# 11. Second text
# ------------------------------
cluster_second_text = html.Div(html.P('Second Text'),style=STYLE_CLUSTER_SECOND_TEXT)
# ------------------------------
# 12. End space
# ------------------------------
cluster_end_space = html.Div(html.P(''),style=STYLE_CLUSTER_END_SPACE,id='empty_space')

# ------------------------------
# 13. Callback
# ------------------------------
# 13.1 Additional data frame to be transformed upon changes in the page.
df_scatter = df_clusters.copy()
# 13.2 Variable to know which Feature is selected.
cl_scatter_feature = 280 # Should be the same as in the line 228.
cl_feature_label = 'dane_doc_31' # Label of variable 280.
@app.callback(
    [Output('cluster_scatter', 'figure'),
     Output('cluster_box', 'figure')],
    [Input('cluster_var_drop', 'value'),
    Input('cluster_radio_log', 'value'),
    Input('cluster_select_drop', 'value'),
    Input('cluster_radio_y', 'value')])
def update_cluster_figures(feature_id,log_value, cluster_value, y_value):
    global df_scatter, cl_scatter_feature, cl_feature_label
    # 1. Determine if there is a change in the feature selection. If so, changes the data frame.
    if feature_id is not None:
        if feature_id == cl_scatter_feature:
            print('Not necessary to update data frame')
        else: # Update the data frame with the selected feature.
            cl_scatter_feature = feature_id
            new_feature_name = df_vars[df_vars['var_id'] == str(feature_id)][['var_name']].reset_index()['var_name'][0]
            cl_feature_label = df_vars[df_vars['var_id'] == str(feature_id)][['Feature']].reset_index()['Feature'][0]
            sql_query = 'select name_municip, desertion_no, desertion_perc, me_cobertura_neta, ' + \
                        'cobertura_rank, desercion_rank, deser_perc_rank, '+ \
                        new_feature_name + ' from cluster_master_table_by_municipio; '
            df_scatter = def_data.runQuery(sql_query)
            for col in ['desertion_no', 'me_cobertura_neta', 'desertion_perc', new_feature_name]:
                df_scatter[col] = df_scatter[col].astype(np.float64)
            df_scatter.rename(columns={
                'name_municip':'Municipio',new_feature_name: cl_feature_label,
                'desertion_no':'# Dropouts','desertion_perc':'% Dropouts',
                'me_cobertura_neta':'Coverage', 'deser_perc_rank':'Cluster',
                "cobertura_rank": "Coverage Type", "desercion_rank": "Desertion Type"
            }, inplace=True)
            print(df_scatter.head())
    # 2. Filter data according to selected cluster.
    if cluster_value is None: # If no filter, then use a copy of data.
        df_scatter_final = df_scatter
    else:
        df_scatter_final = df_scatter[df_scatter['Cluster']==cluster_value]

    # 3. Determine the scale o x-axis: linear or logarithmic
    cl_scale = True if log_value == 'log' else False

    # 4. Make new scatter plot
    new_scatter = px.scatter(df_scatter_final, x=cl_feature_label, y=y_value, log_x=cl_scale)

    # 5. Make new box plot
    new_box = px.box(df_scatter_final, x="Coverage Type", y=cl_feature_label, color="Desertion Type",log_y=cl_scale,
                         points="all", title="Box plot of "+cl_feature_label, hover_data=["Municipio"])
    return [new_scatter,new_box]

# ------------------------------
# 14. Layout
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
    cluster_second_text,
    cluster_end_space
], className="ds4a-body")


