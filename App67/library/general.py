# Basics Requirements
import dash_core_components as dcc
import dash_html_components as html
# import dash_bootstrap_components as dbc
import plotly.express as px
import codecs
from app import app

##############################
# General
##############################
# CONTENTS
#  1. Styles
#  2. Description Text
#  3. Image

# ------------------------------
# 1. Styles
# ------------------------------

# 1.1 Map Styles
STYLE_DESCRIPTION = {
    "position": "absolute",
    "width": "42.5%",
    "height": "400px",
    "left": "15%",
    "top": "160px",
    #"border": "10px solid #e7eff6",
    #"border-radius": "10px",
    'color': '#072552',
    'fontSize': 16,
    'fontWeight': 'bolder'
}

# 1.2 Map Styles
GENERAL_BACKGROUND = {
    "position": "absolute",
    "width": "60%",
    "height": "450px",
    "right": "10%",
    "top": "190px",
    "background-image": 'url(/assets/img/education2.jpg)',
    'background-repeat': 'no-repeat'
}
# ------------------------------
# 2. Description Text
# ------------------------------
text = dcc.Tab(
        label='About',
        value='what-is',
        children=html.Div(className='control-tab', children=[

            html.Br(),
            html.H2(children='Project Description'),
            html.Br(),
            html.P('Scholar desertion is an important phenomenon that affects boys,' 
                   ' girls and teenagers around the globe. In developing countries,' 
                    ' it affects society at different levels as not attending school' 
                    ' impacts the individual’s possibilities to improve his or her wellbeing.' 
                    ' Scholar desertion at younger ages severely limits job opportunities and '
                    'contributes to the propagation of poverty cycles across generations.'
                   ),
            html.P('Considering the relevance of fighting school desertion in Colombia,' 
                    ' we defined a set of questions that, using data-analysis, could help '
                    'the government to better allocate resources and design targeted policies'
                    ' to prevent school dropout.')
        ], style=STYLE_DESCRIPTION)

    )
# ------------------------------
# 3. Images
# ------------------------------
bg = html.Div(style=GENERAL_BACKGROUND)

##############################
# General Layout
##############################
general = html.Div(id='general_description', children=[
    bg,
    text
])