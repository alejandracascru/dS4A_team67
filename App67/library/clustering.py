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
    "height": "470px",
    "left": "7%",
    "top": "140px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}
# 1.2 Map Styles
STYLE_CLUSTER_FIGURE3D = {
    "position": "absolute",
    "width": "86%",
    "height": "450px",
    "left": "7%",
    "top": "620px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.3 First Text
STYLE_CLUSTER_FIRST_TEXT = {
    "position": "absolute",
    "width": "42%",
    "height": "470px",
    "right": "7%",
    "top": "140px"#,
    #"border": "1px solid #e7eff6",
    #"border-radius": "10px"
}

# 1.4 Histogram
STYLE_CLUSTER_HISTOGRAM = {
    "position": "absolute",
    "width": "42%",
    "height": "500px",
    "left": "7%",
    "top": "1080px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px",
    'overflowY': 'scroll'
}

# 1.5 Features
STYLE_CLUSTER_FEATURES = {
    "position": "absolute",
    "width": "42%",
    "height": "500px",
    "right": "7%",
    "top": "1080px"#,
    #"border": "1px solid #e7eff6",
    #"border-radius": "10px"
}

# 1.6 Dropdown
STYLE_CLUSTER_DROPDOWN = {
    "position": "absolute",
    "width": "42%",
    "height": "60px",
    "left": "7%",
    "top": "1600px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.7 Scatterplot
STYLE_CLUSTER_SCATTERPLOT = {
    "position": "absolute",
    "width": "42%",
    "height": "450px",
    "left": "7%",
    "top": "1670px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.8 Boxplot
STYLE_CLUSTER_BOXPLOT= {
    "position": "absolute",
    "width": "42%",
    "height": "440px",
    "right": "7%",
    "top": "1600px",
    "border": "1px solid #e7eff6",
    "border-radius": "10px"
}

# 1.9 Second text
STYLE_CLUSTER_SECOND_TEXT = {
"position": "absolute",
    "width": "42%",
    "height": "200px",
    "right": "7%",
    "top": "2050px"#,
    #"border": "1px solid #e7eff6",
    #"border-radius": "10px"
}

# 1.10 Second text
STYLE_CLUSTER_END_SPACE = {
"position": "absolute",
    "width": "42%",
    "height": "20px",
    "right": "7%",
    "top": "2250px"
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
with open('data/municipios_1mn.json') as geo:
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
size = [4 for i in range(df_clusters.shape[0])]
cl_scatter = px.scatter_3d(df_clusters, x="# Dropouts", y="Coverage", z="% Dropouts", log_x=True,
                           color="Cluster",hover_name="Municipio", size=size,
                           opacity=0.5)
cluster_figure_3D = html.Div([dcc.Graph(figure=cl_scatter, id='cluster_map')],style=STYLE_CLUSTER_FIGURE3D)
# ------------------------------
#  5. First text
# ------------------------------
paragraph01 = '''
A K-means clustering algorithm was applied to group the municipalities using our interest variables: the dropout rate, the number of students that leave the school and the Net Educational Coverage. We found four clusters:

`**Cluster 1 (LD-LC)**`: Municipalities with low desertion and low coverage. It is formed by 270 towns. We see that many of the municipalities of this group are highly rural, and spread across many regions.

`Cluster 2 (LD-HC)`: Municipalities with low desertion and high coverage. 355 towns belong to this group.

**Cluster 3 (HD-LC)**: Municipalities with high desertion and low coverage. Inside of this cluster, there are 242 Towns. In this cluster, we find many municipalities that have had less presence of the government and are affected by poverty and armed conflict.

**Cluster 4 (HD-HC)**: Municipalities with high desertion and high coverage. The size of this group is 253. Many of the departmental capitals and main cities are represented in this cluster.
'''
cluster_first_text = html.Div(dcc.Markdown(paragraph01),style=STYLE_CLUSTER_FIRST_TEXT)
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
paragraph2_01 = 'To obtain the variables that are mostly related to the dropout rate and the coverage percentage, ' + \
             'we executed three machine learning algorithms for classification:'
list2_01 = 'Decision tree: Conditional control algorithm based on a chi-square test to classify a categorical ' + \
           'phenomenon (in our case, the clusters found).'
list2_02 = 'Random Forest: Ensemble learning method based on the implementation of multiple decision trees to ' + \
            'determine the group which a municipality belongs to.'
list2_03 = 'XG-Boost: Ensemble of weak prediction models (in this case, decision trees) to accurately find the ' + \
           'predicted category of a cluster for a given municipality.'
paragraph2_02 = 'Finally, to obtain the weighted importance of each analyzed attribute, we combined the importances ' + \
                'provided by the three methodologies. By using this approach, we guarantee that the variables chosen ' + \
                'are the ones that best explain the clusters independent of the classification technique.'
cluster_features = html.Div([html.P(paragraph2_01),
                             html.Li(list2_01),
                             html.Li(list2_02),
                             html.Li(list2_03),
                             html.P(paragraph2_02)],style=STYLE_CLUSTER_FEATURES)
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
             points="all", title="Box plot of # Teachers (12,13,14) ranking", hover_data=["Municipio"])
cluster_boxplot = html.Div([dcc.Graph(figure=cluster_box, id='cluster_box')],style=STYLE_CLUSTER_BOXPLOT)
# ------------------------------
# 11. Second text
# ------------------------------
cluster_second_text = html.Div(html.P('Second Text'),id='feature_text',style=STYLE_CLUSTER_SECOND_TEXT)
# ------------------------------
# 12. End space
# ------------------------------
cluster_end_space = html.Div(html.P(''),style=STYLE_CLUSTER_END_SPACE,id='empty_space')

# ------------------------------
# 13. Callback
# ------------------------------
# 13.0 Text display according to feature selection
text_list = ['142','18','19','212','218','130','30','150','154','45','280','72','77','132']
text_content = {}
text_content['142'] = '''
    dane_alu_18_p - Percentage of students that study in afternoon sessions.
    We can see that in the cases where the percentage of students enrolled in afternoon sessions is high, desertion percentage increases. This is more evident in municipalities that have high educational coverage. One possible explanation is that those students who study in the afternoon may have to work (or be in charge of household chores) during the mornings. Given their responsibilities, they may be tired when they arrive at school and can be inclined to leave to be full-time in their duties.
'''
text_content['18'] = '''
icbf_tasa_fecun_nin_10_14 - Fecundity rate between children aged between 10 and 14 years.

When analysing the rate of pregnant students aged 10 to 14 years old, the desertion rate tends to be higher than those municipalities where the fecundity rate is lower. The difference is independent of coverage level, which supports that teen and child pregnancy is a critical variable to tackle to reduce desertion. See also the variable “% Fertility children 15-19Y”.
'''
text_content['19'] = '''
icbf_tasa_fecun_nin_15_19 - Fecundity rate between children aged between 15 and 19 years

The fecundity rate of children 15 to 19 shows a similar differentiation across clusters to those found in children between 10 and 14 years old. However, these rates are much higher than the ones of younger children. Using both variables can be very useful to understand dropouts. The first can help classify between the observed clusters, while the second can help explain the variability inside each group. See also the variable “% Fertility children 10-14Y”.
'''
text_content['212'] = '''
me_tamaño_promedio_de_grupo - average size of student groups in the municipality.

The size of the student group assigned to each classroom plays a significant role in differentiating among clusters. We see that dropout is smaller in classes with fewer students. The difference can be explained because, in smaller classrooms, teachers are better able to pay attention to each student and provide specific support. This is true regardless of coverage level points to group size as a relevant variable for desertion.
'''
text_content['218'] = '''
sa_punt_matematicas : Average scores obtained on the standardized SABER test in the field of mathematics.

The standardised test scores in mathematics show a differentiation across clusters which is important only for municipalities with low coverage. This suggests that although academic performance can be relevant to study desertion, the importance of this relation is more related to access to resources and other problems common to rural areas or poverty situations.
'''
text_content['130'] = '''
dane_alu_12_P - Percentage of students that were moved (changed schools).

This variable shows a clear differentiation across clusters which is more critical for desertion than for coverage. This is to be expected as changing schools can be traumatic for many students, and can be a powerful reason to abandon school. It may be useful to give more attention to the reasons that make students change schools (displacement, economic, etc) to get a better understanding of the influence of transfers.
'''
text_content['30'] = '''
cr_homicidio_10mil - Number of murders reported by every 10.000 habitants of the municipality

The municipalities that have a large dropout rate tend to present a higher number of murders by every 10.00 habitants. The variation tends to affect desertion at a larger level and seems invariante to coverage. However we must note that national police variables are greatly under-recorded. This restrains us from giving accurate conclusions, but the variable still gives us an idea of the behaviour of the data.
'''
text_content['150'] = '''
Dane_alu_22_p - Percentage of students enrolled in preschool.

By understanding the percentage of students enrolled in preschool, it can be extracted that the municipalities with high levels of desertion also have more students in kindergarten. In this case, those towns with high desertion rates have a significant difference between low and high coverage. But, in the case of municipalities with low dropout rates, the percentage of students enrolled in preschool doesn’t differ significantly compared to those with high coverage. See also the variable “% Students secondary”.
'''
text_content['154'] = '''
Dane_alu_24_p - Percentage of students enrolled in middle school.

Comparing the percentages of students in middle school with the percentage of students enrolled in preschool, we observe a turnaround in the distribution across the dropout rates. This reversal of tendencies across the proportion of preschoolers and middle schoolers suggests that students dropout occurs mainly during or after completing primary school. See also the variable “% Students preschool”.
'''
text_content['45'] = '''
pobr_imp_cabecer -: Multidimensional index of poverty in the urban center.

A common belief is that a driver of the dropout percentage is poverty. Consistently, the multidimensional poverty index shows a clear influence. Clearly, the higher the poverty measured by the multidimensional index, the more elevated the desertion rate. It happens in municipalities with both high and low coverage rates  with the effect being more drastic on the low coverage side.
'''
text_content['280'] = '''
dane_doc_31_p - percentage of teachers in the highest education and experience tier (12, 13 and 14).

The teachers play a crucial part during the education process and a good and experienced teacher can have a great impact on desertion rates. We see that in the municipalities where the percentage of teachers who are on the higher tiers of the experience ladder (12, 13 or 14 the more experienced teachers), the dropout rate is lower. The previous behaviour is more evident in the towns with low coverage.
'''
text_content['72'] = '''
Dane_tic_01: Average number of computers per every 100 students

The technology inside the schools is also an important driver regarding education and school desertion. As a result, the higher the number of computers that the students can use, the lower the dropout rate. Curiously, Some of the municipalities with high coverage have a lower number of computers per student than those belonging to low coverage rates. The effect of the access to computers and resources is independent of the coverage level, suggesting that technological resources are significant for the reduction of scholar desertion.
'''
text_content['77'] = '''
dane_tic_03_1_p - Percentage of schools with electricity

We can see that municipalities where the amount of schools with access to electricity is lower the desertion percentage is bigger. This is more important for municipalities where educational coverage is low, where we can see that the percentage is much more disperse. This feature is especially important in the cluster of high desertion and low coverage.
'''
text_content['132'] = '''
dane_alu_13_p -Percentage of students displaced / demobilized.

The number of demobilized or displaced students is an important differentiator of clusters with respect to desertion. This suggests that when expanding coverage on the High desertion cluster programs to attend the needs of children affected by armed conflict would be desirable.
'''

# 13.1 Additional data frame to be transformed upon changes in the page.
df_scatter = df_clusters.copy()
# 13.2 Variable to know which Feature is selected.
cl_scatter_feature = 280 # Should be the same as in the line 228.
cl_feature_label = 'dane_doc_31' # Label of variable 280.
@app.callback(#feature_text
    [Output('cluster_scatter', 'figure'),
     Output('cluster_box', 'figure'),
     Output('feature_text', 'children')],
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

    # 6. Second text according to feature selection
    new_second_text = ''
    if feature_id in text_list:
        new_second_text = text_content[feature_id]

    return [new_scatter,new_box,new_second_text]

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


