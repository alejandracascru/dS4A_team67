# Basics Requirements
import dash_core_components as dcc
import dash_html_components as html

from app import app

##############################
# General
##############################
# CONTENTS
#  1. Styles
#  2. Description Text
#  3. Image
#  4. Photos

# ------------------------------
# 1. Styles
# ------------------------------

# 1.1 text
STYLE_DESCRIPTION = {
    "position": "absolute",
    "width": "51%",
    "height": "400px",
    "left": "14%",
    "top": "115px",
    #"border": "10px solid #e7eff6",
    #"border-radius": "10px",
    'color': '#072552',
    'fontSize': 16,
    'text-align': 'justify'
}

# 1.2 Background
GENERAL_BACKGROUND = {
    "position": "absolute",
    "width": "60%",
    "height": "400px",
    "right": "5%",
    "top": "160px",
    "background-image": 'url(/assets/img/education2.jpg)',
    'background-repeat': 'no-repeat'
}

# 1.3 Photo 1
PHOTO_1 = {
    "position": "absolute",
    "left": "9%",
    "top": "445px",
    "width": "9.5%"
}
# 1.3 Photo 1
PHOTO_2 = {
    "position": "absolute",
    "left": "20%",
    "top": "445px",
    "width": "8%"
}
# 1.3 Photo 1
PHOTO_3 = {
    "position": "absolute",
    "left": "30%",
    "top": "445px",
    "width": "8%"
}
# 1.3 Photo 1
PHOTO_4 = {
    "position": "absolute",
    "left": "40%",
    "top": "445px",
    "width": "8%"
}
# 1.3 Photo 1
PHOTO_5 = {
    "position": "absolute",
    "left": "50%",
    "top": "445px",
    "width": "8%"
}
# 1.3 Photo 1
PHOTO_6 = {
    "position": "absolute",
    "left": "60%",
    "top": "445px",
    "width": "8%"
}
# ------------------------------
# 2. Description Text
# ------------------------------
text = dcc.Tab(
        label='About',
        value='what-is',
        children=html.Div(className='control-tab', children=[

            html.Br(),
            html.Br(),
           # html.H2(children='Project Description'),
            #html.Br(),
            html.P('Scholar desertion is an important phenomenon that affects boys, girls and teenagers' 
                   '  around the globe. In developing countries,' 
                    ' it affects society at different levels as not attending school' 
                    ' impacts the individual’s possibilities to improve his or her wellbeing.' 
                    ' Scholar desertion at younger ages severely limits job opportunities and '
                    'contributes to the propagation of poverty cycles across generations.'
                   ),
            html.P('Considering the relevance of fighting school desertion in Colombia, '
                   'we as a participant team of the DS4A program, defined a set of questions, '
                   'that using data-analysis, could help the government to better allocate '
                   'resources and design targeted policies to prevent school dropout.'),
            html.P('We are:')
        ], style=STYLE_DESCRIPTION)

    )
# ------------------------------
# 3. Images
# ------------------------------
bg = html.Div(style=GENERAL_BACKGROUND)

# ------------------------------
# 4. Photos
# ------------------------------
ph1 = html.Div([
    html.Img(src=app.get_asset_url("img/alejandra_c.png"),style=PHOTO_1)
])
ph2 = html.Div([
    html.Img(src=app.get_asset_url("img/profile_sample.png"),style=PHOTO_2)
])
ph3 = html.Div([
    html.Img(src=app.get_asset_url("img/daniel_j_3.png"),style=PHOTO_3)
])
ph4 = html.Div([
    html.Img(src=app.get_asset_url("img/profile_sample.png"),style=PHOTO_4)
])
ph5 = html.Div([
    html.Img(src=app.get_asset_url("img/diego_m.png"),style=PHOTO_5)
])
ph6 = html.Div([
    html.Img(src=app.get_asset_url("img/luis_p.png"),style=PHOTO_6)
])


##############################
# General Layout
##############################
general = html.Div(id='general_description', children=[
    bg,
    ph1,
    ph2,
    ph3,
    ph4,
    ph5,
    ph6,
    text
])
